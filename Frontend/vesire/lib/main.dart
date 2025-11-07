import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'screens/splash_screen.dart';
import 'services/notification_service.dart';
import 'services/connectivity_service.dart';
import 'l10n/app_localizations.dart';
import 'providers/language_provider.dart';
import 'providers/analytics_provider.dart';
import 'screens/auth/login_screen.dart';
import 'screens/auth/signup_screen.dart';

// Global navigator key for showing snackbars from anywhere
final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase with platform-specific options when available.
  try {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
  } catch (e) {
    // If initialization fails (for unsupported platforms or missing values)
    // the app will continue to run in a limited mode. Log the error so it's
    // easier to debug during setup.
    // ignore: avoid_print
    print('Firebase initialize error: $e');
  }

  // Initialize notification service
  await NotificationService().initialize();
  
  // Initialize connectivity service
  await ConnectivityService().initialize();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LanguageProvider()),
        ChangeNotifierProvider(create: (_) => AnalyticsProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    super.initState();
    // Start global connectivity monitoring when app starts
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ConnectivityService().startMonitoring();
      print('🌐 [APP] Global connectivity monitoring started');
    });
  }

  @override
  void dispose() {
    // Clean up connectivity monitoring when app closes
    ConnectivityService().dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<LanguageProvider>(
      builder: (context, languageProvider, child) {
        return MaterialApp(
          navigatorKey: navigatorKey, // Add global navigator key
          title: 'Vesire',
          debugShowCheckedModeBanner: false,
          locale: languageProvider.locale,
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('en', ''),
            Locale('hi', ''),
            Locale('kn', ''),
          ],
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF4CAF50)),
            useMaterial3: true,
            fontFamily: 'Roboto',
            // Smooth page transitions
            pageTransitionsTheme: const PageTransitionsTheme(
              builders: {
                TargetPlatform.android: CupertinoPageTransitionsBuilder(),
                TargetPlatform.iOS: CupertinoPageTransitionsBuilder(),
              },
            ),
            // Smooth and visible animations
            splashFactory: InkRipple.splashFactory,
            splashColor: Colors.green.withOpacity(0.3),
            highlightColor: Colors.green.withOpacity(0.1),
            // Animate card interactions
            cardTheme: CardThemeData(
              elevation: 2,
              shadowColor: Colors.green.withOpacity(0.2),
              shape: const RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(16)),
              ),
            ),
            elevatedButtonTheme: ElevatedButtonThemeData(
              style: ElevatedButton.styleFrom(
                elevation: 3,
                shadowColor: Colors.green.withOpacity(0.4),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 14),
              ),
            ),
          ),
          home: const SplashScreen(),
          routes: {
            '/login': (_) => const LoginScreen(),
            '/signup': (_) => const SignupScreen(),
          },
        );
      },
    );
  }
}
