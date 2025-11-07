import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'scan_screen.dart';
import 'profile_screen.dart';
import 'history_screen.dart';
import 'analytics_screen.dart';
import 'notifications_screen.dart';
import 'garden_screen.dart';
import 'guide_screen.dart';
import 'community_screen.dart';
import 'api_test_screen.dart';
import '../services/connectivity_service.dart';
import '../l10n/app_localizations.dart';
import '../providers/language_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const HomeDashboard(),
    const NotificationsScreen(),
    const ScanScreen(),
    const AnalyticsScreen(),
    const HistoryScreen(),
  ];

  @override
  void initState() {
    super.initState();
    // Check connectivity when dashboard loads
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ConnectivityService().checkConnectivityWithFeedback(context);
      // Start global monitoring (no context needed)
      ConnectivityService().startMonitoring();
    });
  }

  @override
  void dispose() {
    // Don't stop monitoring here - let it run globally
    super.dispose();
  }

  void _onItemTapped(int index) {
    if (index == 2) {
      // Navigate to full screen scanner
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const ScanScreen()),
      ).then((shouldShowAnalytics) {
        // If scan screen returns true, switch to analytics tab
        if (shouldShowAnalytics == true) {
          setState(() {
            _selectedIndex = 3; // Analytics tab
          });
        }
      });
    } else {
      setState(() {
        _selectedIndex = index;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 10,
              offset: const Offset(0, -2),
            ),
          ],
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 12),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildNavItem(Icons.home_rounded, loc.translate('home'), 0),
                _buildNavItem(Icons.notifications_rounded, loc.translate('notifications'), 1),
                _buildScanButton(),
                _buildNavItem(Icons.bar_chart_rounded, loc.translate('analytics'), 3),
                _buildNavItem(Icons.history_rounded, loc.translate('history'), 4),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem(IconData icon, String label, int index) {
    final isSelected = _selectedIndex == index;
    return GestureDetector(
      onTap: () => _onItemTapped(index),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: isSelected ? const Color(0xFF4CAF50) : Colors.transparent,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                icon,
                color: isSelected ? Colors.white : Colors.grey.shade600,
                size: 24,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                color: isSelected ? const Color(0xFF4CAF50) : Colors.grey.shade600,
                fontSize: 11,
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildScanButton() {
    return GestureDetector(
      onTap: () => _onItemTapped(2),
      child: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: const LinearGradient(
            colors: [Color(0xFF4CAF50), Color(0xFF45A049)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF4CAF50).withOpacity(0.4),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: const Icon(Icons.qr_code_scanner_rounded, color: Colors.white, size: 28),
      ),
    );
  }
}

class HomeDashboard extends StatefulWidget {
  const HomeDashboard({super.key});

  @override
  State<HomeDashboard> createState() => _HomeDashboardState();
}

class _HomeDashboardState extends State<HomeDashboard> {
  Future<void> _handleRefresh() async {
    // Check connectivity when user pulls to refresh
    await ConnectivityService().checkConnectivityWithFeedback(context);
    
    // Add any other refresh logic here (e.g., reload data)
    await Future.delayed(const Duration(milliseconds: 500));
  }
  
  void _showLanguageMenu() {
    final languageProvider = Provider.of<LanguageProvider>(context, listen: false);
    final loc = AppLocalizations.of(context)!;
    
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              loc.translate('selectLanguage'),
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 20),
            _buildLanguageOption('English', '🇬🇧', const Locale('en'), languageProvider),
            _buildLanguageOption('हिंदी', '🇮🇳', const Locale('hi'), languageProvider),
            _buildLanguageOption('ಕನ್ನಡ', '🇮🇳', const Locale('kn'), languageProvider),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
  
  Widget _buildLanguageOption(String language, String flag, Locale locale, LanguageProvider languageProvider) {
    final isSelected = languageProvider.locale.languageCode == locale.languageCode;
    return ListTile(
      leading: Text(flag, style: const TextStyle(fontSize: 24)),
      title: Text(
        language,
        style: TextStyle(
          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
          color: isSelected ? const Color(0xFF4CAF50) : Colors.black,
        ),
      ),
      trailing: isSelected
          ? const Icon(Icons.check_circle, color: Color(0xFF4CAF50))
          : null,
      onTap: () {
        languageProvider.setLocale(locale);
        Navigator.pop(context);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    final languageProvider = Provider.of<LanguageProvider>(context);
    
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _handleRefresh,
          color: const Color(0xFF4CAF50),
          backgroundColor: Colors.white,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Garden Illustration Header
                _buildGardenHeader(languageProvider, loc),

                // Stats Grid
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: _buildStatCard(
                              loc.translate('totalScans'),
                              '53',
                              Icons.inventory_2_outlined,
                              const Color(0xFFFFB74D),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: _buildStatCard(
                              loc.translate('healthyPlants'),
                              '40',
                              Icons.spa_outlined,
                              const Color(0xFF66BB6A),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: _buildStatCard(
                              loc.translate('diseasedPlants'),
                              '22',
                              Icons.warning_amber_outlined,
                              const Color(0xFFEF5350),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: _buildStatCard(
                              loc.translate('mostCommonDisease'),
                              'Blight',
                              Icons.bug_report_outlined,
                              const Color(0xFF66BB6A),
                              isDisease: true,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),

                      // Weather Card
                      _buildWeatherCard(loc),

                      const SizedBox(height: 30),

                      // Recent Activity Section
                      _buildSectionTitle(loc.translate('recentActivity')),
                      const SizedBox(height: 16),
                      _buildRecentActivityCard(
                        'Tomato Plant',
                        'Scanned 2 hours ago',
                        'Healthy - No diseases detected',
                        Icons.check_circle,
                        const Color(0xFF4CAF50),
                      ),
                      const SizedBox(height: 12),
                      _buildRecentActivityCard(
                        'Rose Bush',
                        'Scanned yesterday',
                        'Disease detected - Powdery Mildew',
                        Icons.warning_amber_rounded,
                        const Color(0xFFFF9800),
                      ),

                      const SizedBox(height: 30),

                      // Plant Care Tips Section
                      _buildSectionTitle(loc.translate('plantCareTips')),
                      const SizedBox(height: 16),
                      _buildCareTipCard(
                        loc.translate('tipWateringTitle'),
                        loc.translate('tipWateringDesc'),
                        const Color(0xFF2196F3),
                      ),
                      const SizedBox(height: 12),
                      _buildCareTipCard(
                        loc.translate('tipSunlightTitle'),
                        loc.translate('tipSunlightDesc'),
                        const Color(0xFFFFB74D),
                      ),
                      const SizedBox(height: 12),
                      _buildCareTipCard(
                        loc.translate('tipSoilTitle'),
                        loc.translate('tipSoilDesc'),
                        const Color(0xFF66BB6A),
                      ),

                      const SizedBox(height: 30),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.bold,
        color: Color(0xFF1A1A1A),
      ),
    );
  }

  Widget _buildRecentActivityCard(
    String plantName,
    String timeAgo,
    String status,
    IconData icon,
    Color iconColor,
  ) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: iconColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: iconColor, size: 24),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  plantName,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1A1A1A),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  timeAgo,
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  status,
                  style: TextStyle(
                    fontSize: 13,
                    color: iconColor,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
          Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey.shade400),
        ],
      ),
    );
  }

  Widget _buildCareTipCard(String title, String description, Color accentColor) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 4,
            height: 60,
            decoration: BoxDecoration(
              color: accentColor,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1A1A1A),
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  description,
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.grey.shade700,
                    height: 1.4,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGardenHeader(LanguageProvider languageProvider, AppLocalizations loc) {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            const Color(0xFF7CB342),
            const Color(0xFFA5D6A7),
          ],
        ),
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(40),
          bottomRight: Radius.circular(40),
        ),
      ),
      child: Stack(
        children: [
          // Decorative elements
          Positioned(
            top: 20,
            right: 40,
            child: Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: const Color(0xFFFFEB3B).withOpacity(0.9),
                shape: BoxShape.circle,
              ),
            ),
          ),
          Positioned(
            top: 50,
            left: 30,
            child: Icon(
              Icons.cloud,
              color: Colors.white.withOpacity(0.6),
              size: 40,
            ),
          ),
          Positioned(
            top: 80,
            right: 100,
            child: Icon(
              Icons.cloud,
              color: Colors.white.withOpacity(0.5),
              size: 30,
            ),
          ),

          // Content
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 40, 20, 30),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Top Bar with Profile and Language Switcher
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        GestureDetector(
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const ProfileScreen(),
                              ),
                            );
                          },
                          child: Container(
                            width: 45,
                            height: 45,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.1),
                                  blurRadius: 8,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: ClipOval(
                              child: Icon(
                                Icons.person,
                                color: const Color(0xFF4CAF50),
                                size: 28,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              loc.translate('welcome').toUpperCase(),
                              style: const TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w500,
                                color: Color(0xFF2E7D32),
                                letterSpacing: 1,
                              ),
                            ),
                            Text(
                              'Srijan!',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF1A1A1A),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        GestureDetector(
                          onTap: _showLanguageMenu,
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.1),
                                  blurRadius: 8,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(
                                  Icons.language,
                                  color: Color(0xFF4CAF50),
                                  size: 20,
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  languageProvider.getLanguageCode(),
                                  style: const TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Color(0xFF1A1A1A),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        // API Test Button
                        GestureDetector(
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const ApiTestScreen(),
                              ),
                            );
                          },
                          child: Container(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.1),
                                  blurRadius: 8,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: const Icon(
                              Icons.api,
                              color: Color(0xFF4CAF50),
                              size: 20,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Garden illustration with better design
                Center(
                  child: SizedBox(
                    height: 200,
                    child: Stack(
                      children: [
                        // Background layers
                        Positioned(
                          bottom: 0,
                          left: 0,
                          right: 0,
                          child: Container(
                            height: 80,
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                begin: Alignment.topCenter,
                                end: Alignment.bottomCenter,
                                colors: [
                                  const Color(0xFF689F38).withOpacity(0.4),
                                  const Color(0xFF689F38).withOpacity(0.7),
                                ],
                              ),
                              borderRadius: const BorderRadius.vertical(
                                top: Radius.elliptical(250, 60),
                              ),
                            ),
                          ),
                        ),

                        // Decorative plants
                        Positioned(
                          bottom: 25,
                          left: 20,
                          child: _buildPlant(30, const Color(0xFF558B2F)),
                        ),
                        Positioned(
                          bottom: 25,
                          right: 20,
                          child: _buildPlant(25, const Color(0xFF66BB6A)),
                        ),

                        // Main illustration area
                        Positioned(
                          bottom: 20,
                          left: 0,
                          right: 0,
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.end,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              // Left side flowers
                              Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  _buildFlower(35, const Color(0xFFFF6B9D)),
                                  const SizedBox(height: 8),
                                  _buildFlower(28, const Color(0xFFFFB74D)),
                                ],
                              ),
                              const SizedBox(width: 25),

                              // Enhanced gardener character
                              _buildGardenerCharacter(),
                              const SizedBox(width: 25),

                              // Right side garden elements
                              Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Row(
                                    children: [
                                      _buildSunflower(40),
                                      const SizedBox(width: 12),
                                      _buildTreeEnhanced(),
                                    ],
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),

                        // Floating leaves decoration
                        Positioned(
                          top: 30,
                          right: 60,
                          child: _buildLeaf(15, const Color(0xFF66BB6A)),
                        ),
                        Positioned(
                          top: 50,
                          left: 80,
                          child: _buildLeaf(12, const Color(0xFF81C784)),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 25),

                // Quick Actions in Header
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildHeaderQuickAction(
                        Icons.qr_code_scanner_rounded,
                        loc.translate('scan'),
                        () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const ScanScreen()),
                        ),
                      ),
                      _buildHeaderQuickAction(
                        Icons.yard_rounded,
                        loc.translate('garden'),
                        () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const GardenScreen()),
                        ),
                      ),
                      _buildHeaderQuickAction(
                        Icons.book_rounded,
                        loc.translate('guide'),
                        () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const GuideScreen()),
                        ),
                      ),
                      _buildHeaderQuickAction(
                        Icons.people_rounded,
                        loc.translate('community'),
                        () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const CommunityScreen()),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeaderQuickAction(IconData icon, String label, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.08),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    const Color(0xFF4CAF50).withOpacity(0.2),
                    const Color(0xFF66BB6A).withOpacity(0.2),
                  ],
                ),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                icon,
                color: const Color(0xFF2E7D32),
                size: 24,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              label,
              style: const TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w600,
                color: Color(0xFF2E7D32),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlant(double size, Color color) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Leaves
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: size * 0.4,
              height: size * 0.6,
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(size * 0.3),
              ),
            ),
            const SizedBox(width: 2),
            Container(
              width: size * 0.4,
              height: size * 0.6,
              decoration: BoxDecoration(
                color: color.withOpacity(0.8),
                borderRadius: BorderRadius.circular(size * 0.3),
              ),
            ),
          ],
        ),
        // Stem
        Container(
          width: 3,
          height: size * 0.5,
          color: const Color(0xFF558B2F),
        ),
      ],
    );
  }

  Widget _buildFlower(double size, Color color) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Petals
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Container(
              width: size * 0.3,
              height: size * 0.3,
              decoration: const BoxDecoration(
                color: Color(0xFFFFEB3B),
                shape: BoxShape.circle,
              ),
            ),
          ),
        ),
        // Stem
        Container(
          width: 3,
          height: size * 0.8,
          color: const Color(0xFF558B2F),
        ),
      ],
    );
  }

  Widget _buildTreeEnhanced() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Tree crown with layers
        Stack(
          alignment: Alignment.center,
          children: [
            Container(
              width: 45,
              height: 50,
              decoration: BoxDecoration(
                color: const Color(0xFF558B2F),
                borderRadius: BorderRadius.circular(25),
              ),
            ),
            Positioned(
              top: 10,
              child: Container(
                width: 35,
                height: 35,
                decoration: BoxDecoration(
                  color: const Color(0xFF66BB6A),
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
            ),
          ],
        ),
        // Trunk
        Container(
          width: 12,
          height: 25,
          decoration: BoxDecoration(
            color: const Color(0xFF6D4C41),
            borderRadius: BorderRadius.circular(6),
          ),
        ),
      ],
    );
  }

  Widget _buildLeaf(double size, Color color) {
    return Transform.rotate(
      angle: 0.3,
      child: Container(
        width: size,
        height: size * 1.5,
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(size),
        ),
      ),
    );
  }

  Widget _buildGardenerCharacter() {
    return SizedBox(
      width: 100,
      height: 150,
      child: Stack(
        children: [
          // Body with gradient
          Positioned(
            bottom: 0,
            left: 25,
            child: Container(
              width: 50,
              height: 75,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    const Color(0xFF689F38),
                    const Color(0xFF7CB342),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(25),
              ),
            ),
          ),

          // Arms holding pot
          Positioned(
            bottom: 50,
            left: 10,
            child: Container(
              width: 80,
              height: 35,
              decoration: BoxDecoration(
                color: const Color(0xFF689F38),
                borderRadius: BorderRadius.circular(18),
              ),
            ),
          ),

          // Head
          Positioned(
            top: 15,
            left: 30,
            child: Container(
              width: 40,
              height: 40,
              decoration: const BoxDecoration(
                color: Color(0xFFFFCCBC),
                shape: BoxShape.circle,
              ),
              child: Stack(
                children: [
                  // Eyes
                  Positioned(
                    top: 16,
                    left: 10,
                    child: Row(
                      children: [
                        Container(
                          width: 5,
                          height: 5,
                          decoration: const BoxDecoration(
                            color: Color(0xFF5D4037),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 10),
                        Container(
                          width: 5,
                          height: 5,
                          decoration: const BoxDecoration(
                            color: Color(0xFF5D4037),
                            shape: BoxShape.circle,
                          ),
                        ),
                      ],
                    ),
                  ),
                  // Smile
                  Positioned(
                    top: 26,
                    left: 12,
                    child: Container(
                      width: 16,
                      height: 6,
                      decoration: BoxDecoration(
                        border: Border(
                          bottom: BorderSide(
                            color: const Color(0xFF5D4037),
                            width: 2,
                          ),
                        ),
                        borderRadius: const BorderRadius.only(
                          bottomLeft: Radius.circular(8),
                          bottomRight: Radius.circular(8),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Hair with highlights
          Positioned(
            top: 10,
            left: 20,
            child: Container(
              width: 60,
              height: 35,
              decoration: const BoxDecoration(
                color: Color(0xFF6D4C41),
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(35),
                  topRight: Radius.circular(35),
                ),
              ),
            ),
          ),

          // Ponytail
          Positioned(
            top: 25,
            left: 0,
            child: Container(
              width: 28,
              height: 40,
              decoration: BoxDecoration(
                color: const Color(0xFF6D4C41),
                borderRadius: BorderRadius.circular(15),
              ),
            ),
          ),

          // Enhanced plant pot being held
          Positioned(
            bottom: 45,
            left: 32,
            child: _buildPlantPot(),
          ),
        ],
      ),
    );
  }

  Widget _buildPlantPot() {
    return SizedBox(
      width: 40,
      height: 30,
      child: Stack(
        children: [
          // Pot with gradient
          Positioned(
            bottom: 0,
            child: Container(
              width: 40,
              height: 20,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    const Color(0xFF8D6E63),
                    const Color(0xFFA1887F),
                  ],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                ),
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(6),
                  bottomRight: Radius.circular(6),
                ),
              ),
            ),
          ),
          // Small plant with multiple leaves
          Positioned(
            top: 0,
            left: 10,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 8,
                  height: 12,
                  decoration: BoxDecoration(
                    color: const Color(0xFF66BB6A),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                Container(
                  width: 2,
                  height: 5,
                  color: const Color(0xFF558B2F),
                ),
              ],
            ),
          ),
          Positioned(
            top: 3,
            left: 18,
            child: Container(
              width: 6,
              height: 10,
              decoration: BoxDecoration(
                color: const Color(0xFF81C784),
                borderRadius: BorderRadius.circular(3),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSunflower(double size) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Enhanced flower head with petals
        Stack(
          alignment: Alignment.center,
          children: [
            // Outer petals
            Container(
              width: size,
              height: size,
              decoration: BoxDecoration(
                color: const Color(0xFFFFEB3B),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFFFFD54F).withOpacity(0.5),
                    blurRadius: 4,
                    spreadRadius: 2,
                  ),
                ],
              ),
            ),
            // Inner circle
            Container(
              width: size * 0.5,
              height: size * 0.5,
              decoration: BoxDecoration(
                gradient: RadialGradient(
                  colors: [
                    const Color(0xFF6D4C41),
                    const Color(0xFF5D4037),
                  ],
                ),
                shape: BoxShape.circle,
              ),
            ),
          ],
        ),
        // Stem
        Container(
          width: 4,
          height: size * 0.7,
          decoration: BoxDecoration(
            color: const Color(0xFF558B2F),
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        // Leaves
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: size * 0.25,
              height: size * 0.15,
              decoration: BoxDecoration(
                color: const Color(0xFF66BB6A),
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            const SizedBox(width: 4),
            Container(
              width: size * 0.25,
              height: size * 0.15,
              decoration: BoxDecoration(
                color: const Color(0xFF66BB6A),
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStatCard(
    String label,
    String value,
    IconData icon,
    Color color, {
    bool isDisease = false,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: Colors.grey.shade600,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: Text(
                  value,
                  style: TextStyle(
                    fontSize: isDisease ? 16 : 24,
                    fontWeight: FontWeight.bold,
                    color: const Color(0xFF1A1A1A),
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  icon,
                  color: color,
                  size: 20,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildWeatherCard(AppLocalizations loc) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            const Color(0xFFA5D6A7).withOpacity(0.6),
            const Color(0xFF81C784).withOpacity(0.6),
          ],
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '14°',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                    height: 1,
                  ),
                ),
                Text(
                  loc.translate('windy'),
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white.withOpacity(0.9),
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  loc.translate('humidity'),
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.white.withOpacity(0.8),
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  '16:15',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w600,
                    color: Colors.white.withOpacity(0.9),
                  ),
                ),
              ],
            ),
          ),
          Column(
            children: [
              Icon(
                Icons.water_drop_outlined,
                color: Colors.white.withOpacity(0.8),
                size: 40,
              ),
              const SizedBox(height: 20),
              Text(
                'Mon Mar 26',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.white.withOpacity(0.7),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
