import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Row(
                children: [
                  IconButton(
                    onPressed: () => Navigator.pop(context),
                    icon: const Icon(Icons.arrow_back),
                  ),
                  Expanded(
                    child: Text(
                      loc.translate('history'),
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                  IconButton(
                    onPressed: () {
                      // Filter options
                    },
                    icon: const Icon(Icons.filter_list),
                  ),
                ],
              ),
            ),

            // History List
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                itemCount: 10,
                itemBuilder: (context, index) {
                  return _buildHistoryItem(
                    'Plant ${index + 1}',
                    _getPlantType(index),
                    _getTimestamp(index),
                    _getPlantImage(index),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getPlantType(int index) {
    final types = ['Indoor Plant', 'Succulent', 'Herb', 'Flower', 'Tree'];
    return types[index % types.length];
  }

  String _getTimestamp(int index) {
    if (index == 0) return 'Just now';
    if (index < 3) return 'Today';
    if (index < 6) return 'Yesterday';
    return '${index - 5} days ago';
  }

  String _getPlantImage(int index) {
    final images = [
      'https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400',
      'https://images.unsplash.com/photo-1593482892540-73c9be8c2682?w=400',
      'https://images.unsplash.com/photo-1459411621453-7b03977f4baa?w=400',
      'https://images.unsplash.com/photo-1466781783364-36c955e42a7f?w=400',
      'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?w=400',
    ];
    return images[index % images.length];
  }

  Widget _buildHistoryItem(
    String name,
    String type,
    String time,
    String imageUrl,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey.shade200),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.shade100,
            blurRadius: 5,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: Image.network(
              imageUrl,
              width: 70,
              height: 70,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) {
                return Container(
                  width: 70,
                  height: 70,
                  color: Colors.grey.shade300,
                  child: const Icon(Icons.image, color: Colors.grey),
                );
              },
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  type,
                  style: TextStyle(fontSize: 14, color: Colors.grey.shade600),
                ),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Icon(
                      Icons.access_time,
                      size: 14,
                      color: Colors.grey.shade500,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      time,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey.shade500,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          IconButton(
            onPressed: () {
              // View details
            },
            icon: const Icon(Icons.arrow_forward_ios, size: 16),
          ),
        ],
      ),
    );
  }
}
