import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';
import 'package:flutter/material.dart';
import '../utils/snackbar_utils.dart';
import '../main.dart' show navigatorKey;

class ConnectivityService {
  static final ConnectivityService _instance = ConnectivityService._internal();
  factory ConnectivityService() => _instance;
  ConnectivityService._internal();

  final Connectivity _connectivity = Connectivity();
  final InternetConnection _internetConnection = InternetConnection();
  StreamSubscription<List<ConnectivityResult>>? _connectivitySubscription;
  StreamSubscription<InternetStatus>? _internetStatusSubscription;
  
  // Stream controller for connectivity changes
  final StreamController<bool> _connectivityController =
      StreamController<bool>.broadcast();
  
  Stream<bool> get connectivityStream => _connectivityController.stream;
  
  bool _isOnline = true;
  bool get isOnline => _isOnline;
  bool _hasShownInitialStatus = false;
  bool _isMonitoring = false;

  /// Initialize connectivity monitoring
  Future<void> initialize() async {
    // Check initial connectivity status
    await checkConnectivity();
    print('🌐 [CONNECTIVITY] Service initialized. Status: ${_isOnline ? "ONLINE" : "OFFLINE"}');
  }

  /// Check current connectivity status
  /// Uses both device connectivity and actual internet check
  Future<bool> checkConnectivity() async {
    try {
      print('🌐 [CONNECTIVITY] Checking connection...');
      
      // First check device connectivity
      final List<ConnectivityResult> connectivityResults = 
          await _connectivity.checkConnectivity();
      
      if (connectivityResults.contains(ConnectivityResult.none)) {
        print('🌐 [CONNECTIVITY] No network connection');
        _isOnline = false;
        _connectivityController.add(false);
        return false;
      }
      
      // Device has network, verify actual internet access
      final hasInternet = await _internetConnection.hasInternetAccess;
      _isOnline = hasInternet;
      _connectivityController.add(hasInternet);
      print('🌐 [CONNECTIVITY] Network: ${connectivityResults.first.name}, Internet: $hasInternet');
      
      return _isOnline;
    } catch (e) {
      print('🌐 [CONNECTIVITY] ❌ Error checking connectivity: $e');
      _isOnline = false;
      _connectivityController.add(false);
      return false;
    }
  }

  /// Check if connected (alias for checkConnectivity)
  Future<bool> isConnected() async {
    return await checkConnectivity();
  }

  /// Check connectivity and show snackbar
  Future<void> checkConnectivityWithFeedback(BuildContext context) async {
    // Show loading indicator
    _showLoadingIndicator(context);

    // Small delay to show the indicator
    await Future.delayed(const Duration(milliseconds: 500));

    final isConnected = await checkConnectivity();

    // Hide loading indicator
    Navigator.of(context, rootNavigator: true).pop();

    // Show result snackbar
    if (isConnected) {
      SnackBarUtils.showSuccessSnackBar(
        context,
        '🌐 Online Mode - You\'re connected!',
      );
    } else {
      SnackBarUtils.showWarningSnackBar(
        context,
        '📴 Offline Mode - No internet connection',
      );
    }
  }

  /// Show a loading dialog
  void _showLoadingIndicator(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return Dialog(
          backgroundColor: Colors.transparent,
          elevation: 0,
          child: Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF4CAF50)),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Checking connection...',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  /// Start listening to connectivity changes globally
  void startMonitoring() {
    if (_isMonitoring) {
      print('🌐 [CONNECTIVITY] Already monitoring, skipping...');
      return;
    }
    
    print('🌐 [CONNECTIVITY] 🎯 Starting global connectivity monitoring...');
    _isMonitoring = true;
    
    // Listen to internet connection status changes (more reliable)
    _internetStatusSubscription = _internetConnection.onStatusChange.listen(
      (status) {
        final wasOnline = _isOnline;
        _isOnline = status == InternetStatus.connected;
        _connectivityController.add(_isOnline);
        
        print('🌐 [CONNECTIVITY] Status changed: ${_isOnline ? "ONLINE ✅" : "OFFLINE ❌"}');

        // Show snackbar on status change (skip initial status)
        if (_hasShownInitialStatus && wasOnline != _isOnline) {
          _showConnectivitySnackbar(_isOnline);
        } else if (!_hasShownInitialStatus) {
          _hasShownInitialStatus = true;
          // Show initial status after a delay
          Future.delayed(const Duration(seconds: 1), () {
            _showConnectivitySnackbar(_isOnline);
          });
        }
      },
    );
    
    // Also listen to device connectivity changes as backup
    _connectivitySubscription = _connectivity.onConnectivityChanged.listen(
      (List<ConnectivityResult> results) async {
        print('🌐 [CONNECTIVITY] Device connectivity changed: ${results.first.name}');
        if (results.contains(ConnectivityResult.none)) {
          final wasOnline = _isOnline;
          _isOnline = false;
          _connectivityController.add(false);
          
          if (_hasShownInitialStatus && wasOnline != _isOnline) {
            _showConnectivitySnackbar(false);
          }
        } else {
          // Verify internet access when network appears
          await checkConnectivity();
        }
      },
    );
  }

  /// Show connectivity snackbar using global navigator key
  void _showConnectivitySnackbar(bool isOnline) {
    try {
      final context = navigatorKey.currentContext;
      if (context != null && context.mounted) {
        if (isOnline) {
          SnackBarUtils.showSuccessSnackBar(
            context,
            '🌐 Back Online! Internet connected',
          );
        } else {
          SnackBarUtils.showWarningSnackBar(
            context,
            '📴 Connection Lost - Working Offline',
          );
        }
      } else {
        print('🌐 [CONNECTIVITY] ⚠️ No valid context available for snackbar');
      }
    } catch (e) {
      print('🌐 [CONNECTIVITY] ⚠️ Could not show snackbar: $e');
    }
  }

  /// Stop listening to connectivity changes
  void stopMonitoring() {
    print('🌐 [CONNECTIVITY] Stopping monitoring...');
    _connectivitySubscription?.cancel();
    _connectivitySubscription = null;
    _internetStatusSubscription?.cancel();
    _internetStatusSubscription = null;
    _isMonitoring = false;
  }

  /// Clean up resources
  void dispose() {
    stopMonitoring();
    _connectivityController.close();
  }
}
