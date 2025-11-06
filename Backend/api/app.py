"""
AgriScan Backend - Main Flask API Server
RESTful API for plant disease detection with AI model, RAG, and offline support
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import base64
import io
from datetime import datetime
from pathlib import Path

# Import services
from services.model_service import model_service
from services.db_service import db_service
from services.rag_service import rag_service
from config import config

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'model_loaded': model_service.model is not None
    })

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get API information"""
    return jsonify({
        'name': 'AgriScan API',
        'version': '1.0.0',
        'description': 'Plant disease detection API with AI, RAG, and offline support',
        'endpoints': {
            'detection': '/api/detect',
            'diagnosis': '/api/diagnose/<disease_name>',
            'history': '/api/history/<user_id>',
            'diseases': '/api/diseases'
        },
        'model_info': model_service.get_model_info()
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get model information"""
    return jsonify(model_service.get_model_info())

# ============================================================================
# Detection Endpoints
# ============================================================================

@app.route('/api/detect', methods=['POST'])
def detect_disease():
    """
    Detect plant diseases in uploaded image
    
    Request Body:
    {
        "image": "base64_encoded_image",
        "confidence_threshold": 0.5,  // optional
        "save_history": true,  // optional
        "user_id": "user-123"  // optional, required if save_history=true
    }
    
    Response:
    {
        "success": true,
        "detection_id": "uuid",
        "detections": [...],
        "image_size": {...},
        "timing": {...}
    }
    """
    try:
        print('🟢 [FLASK] ========== NEW DETECTION REQUEST ==========')
        print(f'🟢 [FLASK] Request from: {request.remote_addr}')
        
        data = request.get_json()
        
        if not data or 'image' not in data:
            print('🟢 [FLASK] ❌ ERROR: No image data provided')
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        # Get parameters
        image_data = data['image']
        confidence_threshold = data.get('confidence_threshold', config.CONFIDENCE_THRESHOLD)
        save_history = data.get('save_history', False)
        user_id = data.get('user_id')
        
        print(f'🟢 [FLASK] Parameters: confidence={confidence_threshold}, save={save_history}, user={user_id}')
        print(f'🟢 [FLASK] Image data size: {len(image_data)} characters')
        
        # Run detection
        print('🟢 [FLASK] Running TFLite model detection...')
        result = model_service.detect(
            image_data=image_data,
            confidence_threshold=confidence_threshold
        )
        
        if not result['success']:
            print(f'🟢 [FLASK] ❌ Detection failed: {result.get("error")}')
            return jsonify(result), 500
        
        print(f'🟢 [FLASK] ✅ Detection complete: {len(result["detections"])} detections found')
        for i, det in enumerate(result['detections']):
            print(f'🟢 [FLASK]    [{i+1}] {det["class_name"]}: {det["confidence"]:.2%}')
        
        # Generate detection ID
        detection_id = str(uuid.uuid4())
        result['detection_id'] = detection_id
        
        # Save to history if requested
        if save_history and user_id:
            try:
                print(f'🟢 [FLASK] Saving to history for user {user_id}...')
                db_service.save_detection(
                    user_id=user_id,
                    detections=result['detections'],
                    image_base64=image_data,  # Store for offline access
                )
                print('🟢 [FLASK] ✅ Saved to history')
            except Exception as e:
                print(f"🟢 [FLASK] ⚠️ Warning: Failed to save detection: {e}")
        
        print(f'🟢 [FLASK] Sending response with detection_id: {detection_id}')
        print('🟢 [FLASK] ================================================')
        return jsonify(result)
        
    except Exception as e:
        print(f'🟢 [FLASK] ❌ EXCEPTION: {str(e)}')
        print('🟢 [FLASK] ================================================')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/detect/batch', methods=['POST'])
def detect_batch():
    """
    Batch detection for multiple images
    
    Request Body:
    {
        "images": ["base64_1", "base64_2", ...],
        "confidence_threshold": 0.5
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'images' not in data:
            return jsonify({
                'success': False,
                'error': 'No images provided'
            }), 400
        
        images = data['images']
        confidence_threshold = data.get('confidence_threshold', config.CONFIDENCE_THRESHOLD)
        
        results = []
        for i, image_data in enumerate(images):
            result = model_service.detect(
                image_data=image_data,
                confidence_threshold=confidence_threshold
            )
            result['image_index'] = i
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results,
            'total_images': len(images)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Diagnosis Endpoints (RAG Layer)
# ============================================================================

@app.route('/api/diagnose/<disease_name>', methods=['GET'])
def diagnose_disease(disease_name):
    """
    Get disease diagnosis and treatment recommendations
    
    Query Parameters:
    - language: Language code (en, kn) - default: en
    - use_cache: Use cached data - default: true
    
    Response:
    {
        "success": true,
        "disease": {...},
        "source": "cache|knowledge_base|online_llm"
    }
    """
    try:
        language = request.args.get('language', 'en')
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
        result = rag_service.get_diagnosis(
            disease_name=disease_name,
            language=language,
            use_cache=use_cache
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diagnose', methods=['POST'])
def diagnose_disease_post():
    """
    Get diagnosis via POST (for complex requests)
    
    Request Body:
    {
        "disease_name": "Tomato leaf late blight",
        "language": "en",
        "use_cache": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'disease_name' not in data:
            return jsonify({
                'success': False,
                'error': 'No disease_name provided'
            }), 400
        
        result = rag_service.get_diagnosis(
            disease_name=data['disease_name'],
            language=data.get('language', 'en'),
            use_cache=data.get('use_cache', True)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# History Endpoints
# ============================================================================

@app.route('/api/history', methods=['POST'])
def save_detection():
    """
    Save detection to history
    
    Request Body:
    {
        "user_id": "user-123",
        "detections": [...],
        "diagnosis": {...},
        "image_base64": "...",  // optional
        "location": "lat,lng",  // optional
        "notes": "..."  // optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'detections' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        detection_id = db_service.save_detection(
            user_id=data['user_id'],
            detections=data['detections'],
            image_base64=data.get('image_base64'),
            diagnosis=data.get('diagnosis'),
            location=data.get('location'),
            notes=data.get('notes')
        )
        
        return jsonify({
            'success': True,
            'detection_id': detection_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """
    Get user's detection history
    
    Query Parameters:
    - limit: Number of records (default: 50)
    - offset: Offset for pagination (default: 0)
    """
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        history = db_service.get_user_history(user_id, limit, offset)
        
        # Parse JSON fields
        for record in history:
            if record.get('detections'):
                record['detections'] = eval(record['detections'])
            if record.get('diagnosis'):
                record['diagnosis'] = eval(record['diagnosis'])
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<detection_id>', methods=['DELETE'])
def delete_detection(detection_id):
    """Delete detection from history"""
    try:
        deleted = db_service.delete_detection(detection_id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Detection deleted'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Detection not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Disease Information Endpoints
# ============================================================================

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get list of all available diseases"""
    try:
        diseases = rag_service.get_all_diseases()
        
        return jsonify({
            'success': True,
            'diseases': diseases,
            'count': len(diseases)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diseases/search', methods=['GET'])
def search_diseases():
    """
    Search diseases by keyword
    
    Query Parameters:
    - q: Search query
    """
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'No search query provided'
            }), 400
        
        matches = rag_service.search_diseases(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'matches': matches,
            'count': len(matches)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 AgriScan API Server Starting...")
    print("=" * 70)
    print(f"📊 Model loaded: {model_service.model is not None}")
    print(f"🗄️  Database: {config.DATABASE_PATH}")
    print(f"🌐 Server: http://{config.HOST}:{config.PORT}")
    print("=" * 70 + "\n")
    
    # Disable auto-reload to prevent crashes during detection
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=False,  # Changed from config.DEBUG to False
        use_reloader=False  # Disable watchdog file monitoring
    )
