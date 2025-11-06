import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'camera_overlay_test.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AR Cube Placer',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const ARScreen(),
    );
  }
}

class ARScreen extends StatefulWidget {
  const ARScreen({super.key});

  @override
  State<ARScreen> createState() => _ARScreenState();
}

class _ARScreenState extends State<ARScreen> {
  late final WebViewController controller;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _initWebView();
  }

  void _initWebView() {
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (url) {
            setState(() {
              isLoading = false;
            });
          },
        ),
      )
      ..loadHtmlString(_getARHtml());
  }

  String _getARHtml() {
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AR Cube Placer</title>
  <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: Arial, sans-serif;
    }
    model-viewer {
      width: 100%;
      height: 100vh;
      background-color: transparent;
    }
    .controls {
      position: absolute;
      top: 20px;
      left: 20px;
      right: 20px;
      background: rgba(0, 0, 0, 0.7);
      padding: 15px;
      border-radius: 10px;
      color: white;
      z-index: 100;
    }
    .controls h2 {
      margin: 0 0 10px 0;
      font-size: 18px;
    }
    .controls p {
      margin: 5px 0;
      font-size: 14px;
    }
    button {
      background: #2196F3;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 5px;
      font-size: 14px;
      margin-top: 10px;
      cursor: pointer;
    }
    button:active {
      background: #1976D2;
    }
  </style>
</head>
<body>
  <div class="controls">
    <h2> AR Cube Placer</h2>
    <p> Tap "View in your space" button below</p>
    <p> Point camera at floor/surface</p>
    <p> Tap to place the cube!</p>
    <p> Walk around to see it from all angles</p>
  </div>

  <model-viewer
    src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    ar
    ar-modes="scene-viewer webxr quick-look"
    camera-controls
    touch-action="pan-y"
    alt="AR Cube"
    ar-scale="auto"
    loading="eager">
    
    <button slot="ar-button" style="background-color: white; border-radius: 4px; border: none; position: absolute; bottom: 16px; right: 16px; padding: 12px 20px; font-size: 16px;">
       View in your space (AR)
    </button>
  </model-viewer>

  <script>
    const modelViewer = document.querySelector('model-viewer');
    
    // Log when AR is activated
    modelViewer.addEventListener('ar-status', (event) => {
      if (event.detail.status === 'session-started') {
        console.log('AR Session Started!');
      }
    });
  </script>
</body>
</html>
    ''';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('AR Cube Placer - Ready!'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              controller.reload();
            },
          ),
          IconButton(
            icon: const Icon(Icons.camera_alt),
            tooltip: 'Camera Overlay Test',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const CameraOverlayTest(),
                ),
              );
            },
          ),
        ],
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: controller),
          if (isLoading)
            const Center(
              child: CircularProgressIndicator(),
            ),
        ],
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton.extended(
            heroTag: 'camera_test',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const CameraOverlayTest(),
                ),
              );
            },
            label: const Text('Camera Test'),
            icon: const Icon(Icons.camera_alt),
            backgroundColor: Colors.green,
          ),
          const SizedBox(height: 10),
          FloatingActionButton.extended(
            heroTag: 'help',
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('How to Use AR'),
                  content: const Text(
                    '1. Tap "View in your space" button\n'
                    '2. Grant camera permissions\n'
                    '3. Point at floor or flat surface\n'
                    '4. Tap screen to place object\n'
                    '5. Walk around to see from all angles!\n\n'
                    'This uses Google Model Viewer - production ready!',
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Got it!'),
                    ),
                  ],
                ),
              );
            },
            label: const Text('Help'),
            icon: const Icon(Icons.help_outline),
          ),
        ],
      ),
    );
  }
}
