import hashlib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def comparar_senhas(hash_senha, senha_usuario):
    if hash_senha == hashlib.sha256(senha_usuario.encode()).hexdigest():
        return True
    else:
        return False

def Similaridade(text1, text2):
    # Converte os texto para vetores TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])

    # Calcula a similaridade do cosseno dos dois vetores
    similarity = cosine_similarity(vectors)
    return similarity[0][1]