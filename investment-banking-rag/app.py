from flask import Flask, jsonify, render_template, request
from embeddings import get_embedding_model
from vector_store import load_vector_db
from llm import get_qa_chain

app = Flask(__name__)

# Global variables to hold our heavy resources
qa_chain = None

def initialize_app():
    """
    Initializes models and chains on startup.
    """
    global qa_chain
    try:
        embedding_model = get_embedding_model()
        vector_store = load_vector_db(embedding_model)
        qa_chain = get_qa_chain(vector_store)
        print("Application initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize app: {e}")

# Initialize immediately (or you can do this in a @before_first_request)
initialize_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    global qa_chain
    if not qa_chain:
        return jsonify({'answer': 'System not initialized. Check logs.'})

    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'})

    try:
        response = qa_chain.invoke(query)
        answer = response['result']
        
        # Extract source
        source_data = {'content': 'No context found', 'source': 'N/A'}
        if response.get('source_documents'):
            first_doc = response['source_documents'][0]
            source_data['content'] = first_doc.page_content
            source_data['source'] = first_doc.metadata.get('source', 'Unknown')

        return jsonify({
            'answer': answer, 
            'source_document': source_data['content'], 
            'doc': source_data['source']
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'answer': 'Error processing request'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)