import 'package:flutter/material.dart';import 'package:flutter/material.dart';

import 'package:flutter/services.dart';import 'package:flutter/services.dart';

import 'package:arcore_flutter_plugin/arcore_flutter_plugin.dart';import 'package:arcore_flutter_plugin/arcore_flutter_plugin.dart';

import 'package:vector_math/vector_math_64.dart' as vector;import 'package:vector_math/vector_math_64.dart' as vector;



void main() {void main() {

  WidgetsFlutterBinding.ensureInitialized();  runApp(const MyApp());

  runApp(const MyApp());}

}

class MyApp extends StatelessWidget {

class MyApp extends StatelessWidget {  const MyApp({super.key});

  const MyApp({super.key});

  @override

  @override  Widget build(BuildContext context) {

  Widget build(BuildContext context) {    return MaterialApp(

    return MaterialApp(      title: 'AR Cube Test',

      title: 'AR Cube Test',      theme: ThemeData(

      theme: ThemeData(        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),

        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),        useMaterial3: true,

        useMaterial3: true,      ),

      ),      home: const ARCubeScreen(),

      home: const ARCubeScreen(),    );

    );  }

  }}

}

class ARCubeScreen extends StatefulWidget {

class ARCubeScreen extends StatefulWidget {  const ARCubeScreen({super.key});

  const ARCubeScreen({super.key});

  @override

  @override  State<ARCubeScreen> createState() => _ARCubeScreenState();

  State<ARCubeScreen> createState() => _ARCubeScreenState();}

}

class _ARCubeScreenState extends State<ARCubeScreen> {

class _ARCubeScreenState extends State<ARCubeScreen> {  ArCoreController? arCoreController;

  ArCoreController? arCoreController;  int cubeCount = 0;

  int cubeCount = 0;

  @override

  @override  void dispose() {

  void dispose() {    arCoreController?.dispose();

    arCoreController?.dispose();    super.dispose();

    super.dispose();  }

  }

  @override

  void _onArCoreViewCreated(ArCoreController controller) {  Widget build(BuildContext context) {

    arCoreController = controller;    return Scaffold(

    arCoreController!.onPlaneDetected = _handlePlaneDetected;      appBar: AppBar(

    arCoreController!.onPlaneTap = _handlePlaneTap;        backgroundColor: Theme.of(context).colorScheme.inversePrimary,

  }        title: const Text('AR Cube Placement Test'),

      ),

  void _handlePlaneDetected(ArCorePlane plane) {      body: Stack(

    if (mounted) {        children: [

      // Plane detected - you could show a message here          // AR View

    }          ARView(

  }            onARViewCreated: onARViewCreated,

            planeDetectionConfig: PlaneDetectionConfig.horizontalAndVertical,

  void _handlePlaneTap(List<ArCoreHitTestResult> hits) {          ),

    final hit = hits.first;          

    _addCube(hit);          // Instructions overlay

  }          Positioned(

            top: 20,

  void _addCube(ArCoreHitTestResult hit) {            left: 20,

    final material = ArCoreMaterial(            right: 20,

      color: Color.fromARGB(255, 66, 134, 244),            child: Container(

      metallic: 1.0,              padding: const EdgeInsets.all(16),

    );              decoration: BoxDecoration(

                color: Colors.black.withOpacity(0.7),

    final cube = ArCoreCube(                borderRadius: BorderRadius.circular(8),

      materials: [material],              ),

      size: vector.Vector3(0.1, 0.1, 0.1),              child: Column(

    );                crossAxisAlignment: CrossAxisAlignment.start,

                children: [

    final node = ArCoreNode(                  Text(

      shape: cube,                    planesDetected 

      position: hit.pose.translation,                        ? '✅ Surface detected! Tap to place cube.' 

      rotation: hit.pose.rotation,                        : '🔍 Move your phone to detect surfaces...',

    );                    style: const TextStyle(

                      color: Colors.white,

    arCoreController?.addArCoreNode(node);                      fontSize: 16,

                          fontWeight: FontWeight.bold,

    setState(() {                    ),

      cubeCount++;                  ),

    });                  const SizedBox(height: 8),

                  Text(

    if (mounted) {                    'Cubes placed: ${nodes.length}',

      ScaffoldMessenger.of(context).showSnackBar(                    style: const TextStyle(

        SnackBar(                      color: Colors.white70,

          content: Text('Cube #$cubeCount placed!'),                      fontSize: 14,

          duration: const Duration(seconds: 1),                    ),

        ),                  ),

      );                ],

    }              ),

  }            ),

          ),

  void _removeAllCubes() {          

    arCoreController?.dispose();          // Clear button

    arCoreController = null;          if (nodes.isNotEmpty)

    setState(() {            Positioned(

      cubeCount = 0;              bottom: 20,

    });              right: 20,

                  child: FloatingActionButton(

    if (mounted) {                onPressed: removeAllCubes,

      ScaffoldMessenger.of(context).showSnackBar(                backgroundColor: Colors.red,

        const SnackBar(                child: const Icon(Icons.delete),

          content: Text('All cubes removed! Restart AR to place more.'),              ),

          duration: Duration(seconds: 2),            ),

        ),        ],

      );      ),

    }    );

  }  }



  @override  void onARViewCreated(

  Widget build(BuildContext context) {    ARSessionManager arSessionManager,

    return Scaffold(    ARObjectManager arObjectManager,

      appBar: AppBar(    ARAnchorManager arAnchorManager,

        backgroundColor: Theme.of(context).colorScheme.inversePrimary,    ARLocationManager arLocationManager,

        title: const Text('AR Cube Placement Test'),  ) {

      ),    // Store managers

      body: Stack(    this.arSessionManager = arSessionManager;

        children: [    this.arObjectManager = arObjectManager;

          // AR View    this.arAnchorManager = arAnchorManager;

          ArCoreView(

            onArCoreViewCreated: _onArCoreViewCreated,    // Initialize AR session

            enablePlaneRenderer: true,    this.arSessionManager!.onInitialize(

            enableTapRecognizer: true,      showFeaturePoints: false,

          ),      showPlanes: true,

                showWorldOrigin: false,

          // Instructions overlay      handlePans: false,

          Positioned(      handleRotation: false,

            top: 20,    );

            left: 20,

            right: 20,    // Listen for tap events

            child: Container(    this.arSessionManager!.onPlaneOrPointTap = onPlaneOrPointTapped;

              padding: const EdgeInsets.all(16),    

              decoration: BoxDecoration(    // Listen for plane detection

                color: Colors.black.withOpacity(0.7),    this.arObjectManager!.onPanStart = (nodeName) {

                borderRadius: BorderRadius.circular(8),      if (!planesDetected) {

              ),        setState(() {

              child: Column(          planesDetected = true;

                crossAxisAlignment: CrossAxisAlignment.start,        });

                children: [      }

                  const Text(    };

                    '📱 Move phone to detect surfaces...',  }

                    style: TextStyle(

                      color: Colors.white,  Future<void> onPlaneOrPointTapped(List<ARHitTestResult> hitTestResults) async {

                      fontSize: 16,    // Filter for plane results

                      fontWeight: FontWeight.bold,    var singleHitTestResult = hitTestResults.firstWhere(

                    ),      (hitTestResult) => hitTestResult.type == ARHitTestResultType.plane,

                  ),      orElse: () => hitTestResults.first,

                  const SizedBox(height: 8),    );

                  const Text(

                    '👆 Tap on detected surfaces to place cubes',    // Create a cube node at the tapped location

                    style: TextStyle(    var newNode = ARNode(

                      color: Colors.white70,      type: NodeType.localGLTF2,

                      fontSize: 14,      uri: "https://github.com/KhronosGroup/glTF-Sample-Models/raw/master/2.0/Box/glTF-Binary/Box.glb",

                    ),      scale: vector.Vector3(0.2, 0.2, 0.2),

                  ),      position: vector.Vector3(

                  const SizedBox(height: 8),        singleHitTestResult.worldTransform.getColumn(3).x,

                  Text(        singleHitTestResult.worldTransform.getColumn(3).y,

                    'Cubes placed: $cubeCount',        singleHitTestResult.worldTransform.getColumn(3).z,

                    style: const TextStyle(      ),

                      color: Colors.white70,      rotation: vector.Vector4(1.0, 0.0, 0.0, 0.0),

                      fontSize: 14,    );

                    ),

                  ),    // Add node to AR scene

                ],    bool? didAddNode = await arObjectManager!.addNode(newNode);

              ),    

            ),    if (didAddNode == true) {

          ),      nodes.add(newNode);

                setState(() {});

          // Clear button      

          if (cubeCount > 0)      // Show feedback

            Positioned(      if (mounted) {

              bottom: 20,        ScaffoldMessenger.of(context).showSnackBar(

              right: 20,          SnackBar(

              child: FloatingActionButton(            content: Text('Cube #${nodes.length} placed!'),

                onPressed: _removeAllCubes,            duration: const Duration(seconds: 1),

                backgroundColor: Colors.red,          ),

                child: const Icon(Icons.refresh),        );

              ),      }

            ),    }

        ],  }

      ),

    );  Future<void> removeAllCubes() async {

  }    for (var node in nodes) {

}      await arObjectManager!.removeNode(node);

    }
    nodes.clear();
    setState(() {});
    
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('All cubes removed!'),
          duration: Duration(seconds: 1),
        ),
      );
    }
  }
}
