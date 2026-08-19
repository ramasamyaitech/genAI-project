from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from config import LLM_REPO, LLM_CONFIG
from retriever import get_retriever

def get_llm():
    """
    Initializes the CTransformers LLM.
    """
    print(f"Loading LLM: {LLM_REPO}...")
    return CTransformers(
        model=LLM_REPO,
        model_type='mistral',
        config=LLM_CONFIG
    )

def get_qa_chain(vector_store):
    """
    Creates the RetrievalQA chain using the LLM and the dedicated Retriever.
    """
    # 1. Init LLM
    llm = get_llm()
    
    # 2. Init Retriever (from the new file)
    retriever = get_retriever(vector_store)
    
    # 3. Define Prompt
    prompt_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Helpful answer:
"""
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=['context', 'question']
    )

    # 4. Create Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    
    return qa_chain