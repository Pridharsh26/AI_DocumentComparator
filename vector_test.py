from tools.policy_vector_store import PolicyVectorStore


store = PolicyVectorStore()


documents = [
    "OLD POLICY: Employees get 12 leave days",
    "NEW POLICY: Employees get 20 leave days",
    "NEW POLICY: Hybrid work allowed 3 days per week"
]


store.build(documents)


results = store.search(
    "How many leaves do employees get now?"
)


print("Results:")
print(results)