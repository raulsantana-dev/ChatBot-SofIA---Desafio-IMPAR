from langchain_classic.memory import ConversationBufferMemory

memorias = {}

# captura a conversa e armazena na memoria por usuario utilizando session_id
def get_memory(session_id: str) -> ConversationBufferMemory:
    if session_id not in memorias:
        memorias[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return memorias[session_id]

#Salva memoria do usuario
def salvar_memoria(session_id: str, pergunta: str, resposta: str):
    memory = get_memory(session_id)
    memory.save_context(
        {"input": pergunta},
        {"output": resposta}
    )
