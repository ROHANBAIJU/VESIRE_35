import 'dart:io';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../services/notification_service.dart';
import '../services/api_service.dart';
import '../utils/snackbar_utils.dart';
import '../models/detection_response.dart';
import '../models/diagnosis_response.dart';
import 'package:provider/provider.dart';
import '../providers/language_provider.dart';
import '../providers/analytics_provider.dart';
import '../widgets/markdown_text.dart';
import 'analytics_screen.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> with WidgetsBindingObserver {
  CameraController? _cameraController;
  List<CameraDescription> _cameras = [];
  bool _isCameraInitialized = false;
  bool _isDetecting = false;
  File? _lastCapturedImage;
  final ApiService _apiService = ApiService();
  bool _isFlashOn = false;
  
  // Real-time detection state
  Timer? _detectionTimer;
  DetectionResponse? _latestDetection;
  bool _showNavigationPrompt = false;
  bool _isRealTimeDetecting = false;
  bool _isGettingDiagnosis = false;
  DiagnosisResponse? _currentDiagnosis;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _initializeCamera();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _detectionTimer?.cancel();
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final CameraController? cameraController = _cameraController;

    if (cameraController == null || !cameraController.value.isInitialized) {
      return;
    }

    if (state == AppLifecycleState.inactive) {
      // Stop detection timer first
      _detectionTimer?.cancel();
      _detectionTimer = null;
      // Then dispose camera
      cameraController.dispose();
      setState(() {
        _isCameraInitialized = false;
      });
    } else if (state == AppLifecycleState.resumed) {
      _initializeCamera();
    }
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras.isEmpty) {
        SnackBarUtils.showErrorSnackBar(
          context,
          'No camera found on this device',
        );
        return;
      }

      _cameraController = CameraController(
        _cameras.first,
        ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );

      await _cameraController!.initialize();

      if (mounted) {
        setState(() {
          _isCameraInitialized = true;
        });
        
        // Start real-time detection
        _startRealTimeDetection();
      }
    } catch (e) {
      print('Error initializing camera: $e');
      SnackBarUtils.showErrorSnackBar(
        context,
        'Failed to initialize camera: $e',
      );
    }
  }
  
  void _startRealTimeDetection() {
    print('🚀 [FLUTTER] Starting real-time detection...');
    _detectionTimer = Timer.periodic(const Duration(seconds: 5), (timer) async {  // Changed from 3 to 5 seconds
      if (!mounted) {
        timer.cancel();
        return;
      }
      
      // CHECK: Camera controller must exist AND be initialized AND not disposed
      if (_cameraController == null || 
          !_cameraController!.value.isInitialized || 
          !_isCameraInitialized || 
          _isDetecting || 
          _isRealTimeDetecting) {
        print('⏸️ [FLUTTER] Skipping detection cycle (camera not ready)');
        return;
      }
      
      try {
        if (!mounted) return;
        setState(() => _isRealTimeDetecting = true);
        
        print('📸 [FLUTTER] Attempting to capture frame...');
        
        // Double-check before capture
        if (_cameraController == null || !_cameraController!.value.isInitialized) {
          print('❌ [FLUTTER] Camera controller disposed before capture');
          setState(() => _isRealTimeDetecting = false);
          return;
        }
        
        // Capture frame
        final XFile image = await _cameraController!.takePicture();
        final File imageFile = File(image.path);
        
        print('📸 [FLUTTER] Frame captured successfully, sending to backend...');
        
        // Send to backend for detection
        final response = await _apiService.detectDisease(
          imageFile,
          confidenceThreshold: 0.4,
          userId: 'user-123',
          saveHistory: false,
        );
        
        print('✅ [FLUTTER] Backend response received: ${response.detections.length} detections');
        
        if (!mounted) {
          imageFile.delete();
          return;
        }
        
        if (response.detections.isNotEmpty) {
          setState(() {
            _latestDetection = response;
          });
          print('🎯 [FLUTTER] Detections found: ${response.detections.map((d) => '${d.className}(${(d.confidence * 100).toStringAsFixed(1)}%)').join(', ')}');
          
          // Trigger RAG diagnosis (async)
          _triggerDiagnosisAndShowButton(response.detections.first.className);
        } else {
          setState(() {
            _latestDetection = null;
            _showNavigationPrompt = false;
          });
        }
        
        // Clean up temp file
        imageFile.delete();
        
      } catch (e) {
        print('❌ [FLUTTER] Real-time detection error: $e');
      } finally {
        if (mounted) {
          setState(() => _isRealTimeDetecting = false);
        }
      }
    });
  }
  
  void _triggerDiagnosisAndShowButton(String diseaseName) async {
    if (_isGettingDiagnosis) return; // Don't trigger multiple times
    if (!mounted) return;
    
    setState(() {
      _isGettingDiagnosis = true;
      _showNavigationPrompt = false;
    });
    
    print('🤖 [FLUTTER] Triggering RAG diagnosis for: $diseaseName');
    
    try {
      final languageProvider = Provider.of<LanguageProvider>(context, listen: false);
      final languageCode = languageProvider.locale.languageCode;
      
      // Call RAG service
      final diagnosisResult = await _apiService.getDiagnosisWithSource(
        diseaseName,
        language: languageCode,
        useCache: true,
      );
      
      if (!mounted) return; // Check after async operation
      
      final diagnosis = diagnosisResult['diagnosis'] as DiagnosisResponse?;
      
      if (diagnosis != null) {
        print('✅ [FLUTTER] RAG diagnosis received! Source: ${diagnosisResult['source']}');
        
        // Update analytics provider with the data
        final analyticsProvider = Provider.of<AnalyticsProvider>(context, listen: false);
        analyticsProvider.updateFromDetection(
          plantName: diagnosis.disease.name,
          scientificName: diagnosis.disease.scientificName,
          aiConfidence: _latestDetection!.detections.first.confidence * 100,
          aiSummary: diagnosis.disease.description,
          careRecommendations: diagnosis.disease.careRecommendations.isNotEmpty 
              ? diagnosis.disease.careRecommendations 
              : diagnosis.disease.prevention,
        );
        
        if (mounted) {
          setState(() {
            _currentDiagnosis = diagnosis;
            _showNavigationPrompt = true; // NOW show the button
          });
        }
      }
      
    } catch (e) {
      print('❌ [FLUTTER] RAG diagnosis error: $e');
    } finally {
      if (mounted) {
        setState(() => _isGettingDiagnosis = false);
      }
    }
  }

  Future<void> _toggleFlash() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      return;
    }

    try {
      if (_isFlashOn) {
        await _cameraController!.setFlashMode(FlashMode.off);
      } else {
        await _cameraController!.setFlashMode(FlashMode.torch);
      }

      setState(() {
        _isFlashOn = !_isFlashOn;
      });
    } catch (e) {
      print('Error toggling flash: $e');
    }
  }

  Future<void> _captureAndDetect() async {
    if (_cameraController == null ||
        !_cameraController!.value.isInitialized ||
        _isDetecting) {
      return;
    }

    setState(() {
      _isDetecting = true;
    });

    try {
      // Show scanning snackbar
      SnackBarUtils.showInfoSnackBar(
        context,
        'Scanning plant...',
      );

      // Capture image
      final XFile image = await _cameraController!.takePicture();
      final File imageFile = File(image.path);

      setState(() {
        _lastCapturedImage = imageFile;
      });

      // Call API for detection
      final response = await _apiService.detectDisease(
        imageFile,
        confidenceThreshold: 0.5,
        userId: 'user-123',
        saveHistory: false,
      );

      if (response.detections.isEmpty) {
        SnackBarUtils.showWarningSnackBar(
          context,
          'No diseases detected in this image',
        );
        setState(() {
          _isDetecting = false;
        });
        return;
      }

      // Update UI with detections
      setState(() {
        _isDetecting = false;
      });

      // Show success snackbar
      SnackBarUtils.showSuccessSnackBar(
        context,
        'Detected ${response.detections.length} disease(s)!',
      );

      // Show local notification
      await NotificationService().showScanCompleteNotification(
        response.detections.first.className,
      );

      // Wait a bit then show result
      await Future.delayed(const Duration(milliseconds: 500));
      _showResultScreen(response);
    } catch (e) {
      print('Error detecting disease: $e');
      SnackBarUtils.showErrorSnackBar(
        context,
        'Detection failed: ${e.toString()}',
      );
      setState(() {
        _isDetecting = false;
      });
    }
  }

  void _showResultScreen(DetectionResponse response) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => DetectionResultScreen(
          imageFile: _lastCapturedImage!,
          response: response,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Full-screen camera preview
          if (_isCameraInitialized && _cameraController != null)
            SizedBox.expand(
              child: FittedBox(
                fit: BoxFit.cover,
                child: SizedBox(
                  width: _cameraController!.value.previewSize!.height,
                  height: _cameraController!.value.previewSize!.width,
                  child: CameraPreview(_cameraController!),
                ),
              ),
            )
          else
            Container(
              width: double.infinity,
              height: double.infinity,
              color: Colors.black87,
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      'Initializing camera...',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white.withOpacity(0.7),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // Real-time bounding boxes overlay
          if (_latestDetection != null && _cameraController != null)
            Positioned.fill(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  final screenWidth = constraints.maxWidth;
                  final screenHeight = constraints.maxHeight;
                  
                  return Stack(
                    children: _latestDetection!.detections.map((detection) {
                      // YOLO format: center_x, center_y, width, height (normalized 0-1)
                      final centerX = detection.boundingBox.x * screenWidth;
                      final centerY = detection.boundingBox.y * screenHeight;
                      final boxWidth = detection.boundingBox.width * screenWidth;
                      final boxHeight = detection.boundingBox.height * screenHeight;
                      
                      final left = centerX - boxWidth / 2;
                      final top = centerY - boxHeight / 2;
                      
                      return Positioned(
                        left: left,
                        top: top,
                        child: Container(
                          width: boxWidth,
                          height: boxHeight,
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: Colors.red, // RED BOXES as requested
                              width: 3,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Stack(
                            children: [
                              // Label with confidence - position at top
                              Positioned(
                                top: -35,
                                left: 0,
                                child: Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 10,
                                    vertical: 6,
                                  ),
                                  decoration: BoxDecoration(
                                    color: Colors.red, // RED background
                                    borderRadius: BorderRadius.circular(6),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black.withOpacity(0.3),
                                        blurRadius: 4,
                                        offset: const Offset(0, 2),
                                      ),
                                    ],
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Text(
                                        detection.className,
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontSize: 13,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      Text(
                                        '${(detection.confidence * 100).toStringAsFixed(1)}% confidence',
                                        style: TextStyle(
                                          color: Colors.white.withOpacity(0.9),
                                          fontSize: 11,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    }).toList(),
                  );
                },
              ),
            ),
          
          // Floating navigation button (appears after detection and RAG is called)
          if (_showNavigationPrompt && _latestDetection != null && _currentDiagnosis != null)
            Positioned(
              bottom: 120,
              left: 20,
              right: 20,
              child: Material(
                color: Colors.transparent,
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        Colors.green.shade600,
                        Colors.green.shade700,
                      ],
                    ),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.green.withOpacity(0.4),
                        blurRadius: 15,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(
                          Icons.analytics_outlined,
                          color: Colors.white,
                          size: 32,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text(
                              '✓ Detection Complete',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 15,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'AI diagnosis ready to view',
                              style: TextStyle(
                                color: Colors.white.withOpacity(0.9),
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                      ElevatedButton.icon(
                        onPressed: () {
                          // Navigate to analytics screen
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const AnalyticsScreen(),
                            ),
                          );
                        },
                        icon: const Icon(Icons.arrow_forward, size: 18),
                        label: const Text('View'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: Colors.green.shade700,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 20,
                            vertical: 12,
                          ),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(25),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          
          // Loading indicator when getting diagnosis
          if (_isGettingDiagnosis && _latestDetection != null)
            Positioned(
              bottom: 120,
              left: 20,
              right: 20,
              child: Material(
                color: Colors.transparent,
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        Colors.purple.shade600,
                        Colors.purple.shade700,
                      ],
                    ),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.purple.withOpacity(0.4),
                        blurRadius: 15,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      const SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(
                          strokeWidth: 3,
                          valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      ),
                      const SizedBox(width: 20),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Text(
                              '🤖 AI Diagnosis',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 15,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Getting treatment recommendations...',
                              style: TextStyle(
                                color: Colors.white.withOpacity(0.9),
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

          // Top bar
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(
                      Icons.close,
                      color: Colors.white,
                      size: 30,
                    ),
                  ),
                  IconButton(
                    onPressed: _toggleFlash,
                    icon: Icon(
                      _isFlashOn ? Icons.flash_on : Icons.flash_off,
                      color: Colors.white,
                      size: 30,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Bottom controls
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      _isDetecting
                          ? 'Analyzing...'
                          : 'Position plant within frame',
                      style: TextStyle(
                        color: Colors.white.withOpacity(0.9),
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 24),
                    // Capture button
                    GestureDetector(
                      onTap: _isDetecting ? null : _captureAndDetect,
                      child: Container(
                        width: 70,
                        height: 70,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: _isDetecting
                                ? Colors.grey
                                : Colors.white,
                            width: 4,
                          ),
                        ),
                        child: Container(
                          margin: const EdgeInsets.all(6),
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: _isDetecting
                                ? Colors.grey
                                : const Color(0xFF4CAF50),
                          ),
                          child: _isDetecting
                              ? const Padding(
                                  padding: EdgeInsets.all(12.0),
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    valueColor: AlwaysStoppedAnimation<Color>(
                                      Colors.white,
                                    ),
                                  ),
                                )
                              : null,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

}

// Detection Result Screen
class DetectionResultScreen extends StatefulWidget {
  final File imageFile;
  final DetectionResponse response;

  const DetectionResultScreen({
    super.key,
    required this.imageFile,
    required this.response,
  });

  @override
  State<DetectionResultScreen> createState() => _DetectionResultScreenState();
}

class _DetectionResultScreenState extends State<DetectionResultScreen> {
  DiagnosisResponse? _diagnosis;
  bool _isLoadingDiagnosis = false;
  String _diagnosisSource = 'unknown'; // 'cache', 'knowledge_base', 'online_llm', 'synthetic'
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    if (widget.response.detections.isNotEmpty) {
      _loadDiagnosis();
    }
  }

  Future<Size> _getImageSize(File imageFile) async {
    final completer = Completer<Size>();
    final image = Image.file(imageFile);
    image.image.resolve(const ImageConfiguration()).addListener(
      ImageStreamListener((ImageInfo info, bool _) {
        completer.complete(
          Size(
            info.image.width.toDouble(),
            info.image.height.toDouble(),
          ),
        );
      }),
    );
    return completer.future;
  }

  Future<void> _loadDiagnosis() async {
    setState(() {
      _isLoadingDiagnosis = true;
    });

    try {
      // Get the current language from provider
      final languageProvider = Provider.of<LanguageProvider>(context, listen: false);
      final languageCode = languageProvider.locale.languageCode;
      
      final firstDetection = widget.response.detections.first;
      
      // Try to get diagnosis - first with cache, then online
      final diagnosisResult = await _apiService.getDiagnosisWithSource(
        firstDetection.className,
        language: languageCode,
        useCache: true,
      );

      setState(() {
        _diagnosis = diagnosisResult['diagnosis'] as DiagnosisResponse?;
        _diagnosisSource = diagnosisResult['source'] as String;
        _isLoadingDiagnosis = false;
      });
    } catch (e) {
      print('Error loading diagnosis: $e');
      setState(() {
        _isLoadingDiagnosis = false;
      });
      SnackBarUtils.showErrorSnackBar(
        context,
        'Failed to load diagnosis',
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenSize = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Colors.black,
      body: Column(
        children: [
          // Image with bounding boxes
          SizedBox(
            height: screenSize.height * 0.5,
            child: LayoutBuilder(
              builder: (context, constraints) {
                return Stack(
                  children: [
                    // Image
                    Positioned.fill(
                      child: Image.file(
                        widget.imageFile,
                        fit: BoxFit.contain,
                      ),
                    ),

                    // Bounding boxes overlay - Using FutureBuilder to get image dimensions
                    FutureBuilder<Size>(
                      future: _getImageSize(widget.imageFile),
                      builder: (context, snapshot) {
                        if (!snapshot.hasData) {
                          return const SizedBox.shrink();
                        }

                        final imageSize = snapshot.data!;
                        final imageAspectRatio = imageSize.width / imageSize.height;
                        final containerAspectRatio = constraints.maxWidth / constraints.maxHeight;

                        double renderWidth, renderHeight, offsetX, offsetY;

                        if (imageAspectRatio > containerAspectRatio) {
                          // Image is wider - fit to width
                          renderWidth = constraints.maxWidth;
                          renderHeight = constraints.maxWidth / imageAspectRatio;
                          offsetX = 0;
                          offsetY = (constraints.maxHeight - renderHeight) / 2;
                        } else {
                          // Image is taller - fit to height
                          renderHeight = constraints.maxHeight;
                          renderWidth = constraints.maxHeight * imageAspectRatio;
                          offsetX = (constraints.maxWidth - renderWidth) / 2;
                          offsetY = 0;
                        }

                        return Stack(
                          children: widget.response.detections.map((detection) {
                            final box = detection.boundingBox;

                            // Calculate positions based on normalized coordinates (0-1)
                            // YOLO format: x, y are center coordinates, width and height are relative
                            final centerX = box.x * renderWidth + offsetX;
                            final centerY = box.y * renderHeight + offsetY;
                            final boxWidth = box.width * renderWidth;
                            final boxHeight = box.height * renderHeight;

                            final left = centerX - boxWidth / 2;
                            final top = centerY - boxHeight / 2;

                            return Positioned(
                              left: left,
                              top: top,
                              child: Container(
                                width: boxWidth,
                                height: boxHeight,
                                decoration: BoxDecoration(
                                  border: Border.all(
                                    color: const Color(0xFF00FF00),
                                    width: 3,
                                  ),
                                ),
                                child: Stack(
                                  children: [
                                    // Label background at top-left
                                    Positioned(
                                      left: 0,
                                      top: 0,
                                      child: Container(
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 8,
                                          vertical: 4,
                                        ),
                                        decoration: BoxDecoration(
                                          color: const Color(0xFF00FF00),
                                          borderRadius: const BorderRadius.only(
                                            bottomRight: Radius.circular(8),
                                          ),
                                        ),
                                        child: Column(
                                          mainAxisSize: MainAxisSize.min,
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              detection.className,
                                              style: const TextStyle(
                                                color: Colors.black,
                                                fontSize: 12,
                                                fontWeight: FontWeight.bold,
                                              ),
                                            ),
                                            Text(
                                              '${(detection.confidence * 100).toStringAsFixed(1)}%',
                                              style: const TextStyle(
                                                color: Colors.black87,
                                                fontSize: 10,
                                                fontWeight: FontWeight.w600,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        );
                      },
                    ),

                    // Top bar
                    Positioned.fill(
                      child: SafeArea(
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              IconButton(
                                onPressed: () => Navigator.pop(context),
                                icon: const Icon(
                                  Icons.close,
                                  color: Colors.white,
                                  size: 30,
                                ),
                              ),
                              IconButton(
                                onPressed: () {
                                  // Share functionality
                                },
                                icon: const Icon(
                                  Icons.share,
                                  color: Colors.white,
                                  size: 30,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                );
              },
            ),
          ),

          // Diagnosis information
          Expanded(
            child: Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.vertical(
                  top: Radius.circular(30),
                ),
              ),
              child: _isLoadingDiagnosis
                  ? const Center(
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(
                          Color(0xFF4CAF50),
                        ),
                      ),
                    )
                  : _diagnosis != null
                      ? _buildDiagnosisContent()
                      : _buildDetectionsOnly(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDetectionsOnly() {
    return ListView(
      padding: const EdgeInsets.all(24),
      children: [
        const Text(
          'Detections',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1A1A1A),
          ),
        ),
        const SizedBox(height: 20),
        ...widget.response.detections.map((detection) {
          return Container(
            margin: const EdgeInsets.only(bottom: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.grey.shade50,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.grey.shade200),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  detection.className,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'Confidence: ${(detection.confidence * 100).toStringAsFixed(1)}%',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade700,
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ],
    );
  }

  Widget _buildDiagnosisContent() {
    final disease = _diagnosis!.disease;

    return ListView(
      padding: const EdgeInsets.all(24),
      children: [
        // Source indicator badge
        Row(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: _getSourceColor(_diagnosisSource).withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: _getSourceColor(_diagnosisSource),
                  width: 1.5,
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    _getSourceIcon(_diagnosisSource),
                    color: _getSourceColor(_diagnosisSource),
                    size: 16,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    _getSourceLabel(_diagnosisSource),
                    style: TextStyle(
                      color: _getSourceColor(_diagnosisSource),
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),

        // Disease name
        Text(
          disease.name,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1A1A1A),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          disease.scientificName,
          style: TextStyle(
            fontSize: 14,
            fontStyle: FontStyle.italic,
            color: Colors.grey.shade600,
          ),
        ),
        const SizedBox(height: 16),

        // Severity badge
        Row(
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: _getSeverityColor(disease.severity).withOpacity(0.2),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: _getSeverityColor(disease.severity),
                  width: 1.5,
                ),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.warning_amber,
                    color: _getSeverityColor(disease.severity),
                    size: 16,
                  ),
                  const SizedBox(width: 6),
                  Text(
                    '${disease.severity.toUpperCase()} Severity',
                    style: TextStyle(
                      color: _getSeverityColor(disease.severity),
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 20),

        // Description with markdown support
        _buildMarkdownSection(
          'Description',
          Icons.info_outline,
          disease.description,
        ),

        // Symptoms
        _buildMarkdownListSection(
          'Symptoms',
          Icons.medical_services_outlined,
          disease.symptoms,
        ),

        // Care Recommendations (from Gemini)
        if (disease.careRecommendations.isNotEmpty)
          _buildMarkdownListSection(
            '🤖 AI Care Recommendations',
            Icons.auto_awesome,
            disease.careRecommendations,
            isAI: true,
          ),

        // Treatment
        if (disease.treatment.organic.isNotEmpty)
          _buildMarkdownListSection(
            'Organic Treatment',
            Icons.eco_outlined,
            disease.treatment.organic,
          ),

        if (disease.treatment.chemical.isNotEmpty)
          _buildMarkdownListSection(
            'Chemical Treatment',
            Icons.science_outlined,
            disease.treatment.chemical,
          ),

        if (disease.treatment.cultural.isNotEmpty)
          _buildMarkdownListSection(
            'Cultural Practices',
            Icons.agriculture_outlined,
            disease.treatment.cultural,
          ),

        // Prevention
        _buildMarkdownListSection(
          'Prevention',
          Icons.shield_outlined,
          disease.prevention,
        ),

        const SizedBox(height: 30),

        // Action buttons
        Row(
          children: [
            Expanded(
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.pop(context);
                  Navigator.pop(context);
                },
                icon: const Icon(Icons.home),
                label: const Text('Go Home'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4CAF50),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  String _getSourceLabel(String source) {
    switch (source) {
      case 'online_llm':
        return '🌐 Online AI (Gemini)';
      case 'cache':
        return '💾 Cached Data';
      case 'knowledge_base':
        return '📚 Knowledge Base';
      default:
        return '📱 Offline Data';
    }
  }

  IconData _getSourceIcon(String source) {
    switch (source) {
      case 'online_llm':
        return Icons.cloud_done;
      case 'cache':
        return Icons.storage;
      case 'knowledge_base':
        return Icons.book;
      default:
        return Icons.offline_bolt;
    }
  }

  Color _getSourceColor(String source) {
    switch (source) {
      case 'online_llm':
        return Colors.purple.shade600;
      case 'cache':
        return Colors.blue.shade600;
      case 'knowledge_base':
        return Colors.orange.shade600;
      default:
        return Colors.grey.shade600;
    }
  }

  Widget _buildMarkdownSection(String title, IconData icon, String content) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: const Color(0xFF4CAF50), size: 20),
              const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1A1A1A),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          MarkdownText(
            text: content,
            baseStyle: TextStyle(
              fontSize: 14,
              color: Colors.grey.shade700,
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMarkdownListSection(
    String title, 
    IconData icon, 
    List<String> items,
    {bool isAI = false}
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isAI ? Colors.purple.shade50 : Colors.grey.shade50,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isAI ? Colors.purple.shade200 : Colors.grey.shade200,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                icon, 
                color: isAI ? Colors.purple.shade600 : const Color(0xFF4CAF50), 
                size: 20,
              ),
              const SizedBox(width: 8),
              Text(
                title,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: isAI ? Colors.purple.shade900 : const Color(0xFF1A1A1A),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ...items.map((item) {
            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    margin: const EdgeInsets.only(top: 6),
                    width: 6,
                    height: 6,
                    decoration: BoxDecoration(
                      color: isAI ? Colors.purple.shade600 : const Color(0xFF4CAF50),
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: MarkdownText(
                      text: item,
                      baseStyle: TextStyle(
                        fontSize: 14,
                        color: Colors.grey.shade700,
                        height: 1.5,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }

  Color _getSeverityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'high':
        return Colors.red.shade700;
      case 'medium':
        return Colors.orange.shade700;
      case 'low':
        return Colors.green.shade700;
      default:
        return Colors.grey.shade700;
    }
  }
}
