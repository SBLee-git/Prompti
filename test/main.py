from backend.generator.chain import get_jd_chain
from dotenv import load_dotenv
load_dotenv()

test_input = {
    "position": "데이터 엔지니어",
    "experience": "3~5년"
}

chain = get_jd_chain()
generated_jd = chain(test_input)  

print("📌 생성된 직무 기술서:")
print(generated_jd)
