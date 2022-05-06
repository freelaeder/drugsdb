import uuid
name = 'abc'
namespace = 'xyz'

print(uuid.uuid1())
print(uuid.uuid3(uuid.NAMESPACE_DNS, name))
print(uuid.uuid3(uuid.NAMESPACE_DNS, namespace))
print(uuid.uuid4())
print(uuid.uuid5(uuid.NAMESPACE_URL, name))
print(uuid.uuid5(uuid.NAMESPACE_URL, namespace))
# f080ddfc-cc7b-11ec-a0c2-ad5b4561f788
# 5bd670ce-29c8-3369-a8a1-10ce44c7259e
# f7b4c458-3fd5-3239-8b7e-3df3bb620d8f
# df4d0388-3294-41ca-8035-d46bd0a07c37
# 68661508-f3c4-55b4-945d-ae2b4dfe5db4
# 9b9a684f-4201-5785-9966-667603a165cf

# fe2af6e0-cc7b-11ec-a0c2-ad5b4561f788
# 5bd670ce-29c8-3369-a8a1-10ce44c7259e
# f7b4c458-3fd5-3239-8b7e-3df3bb620d8f
# 816d1f2f-6455-4949-ac9f-884b7a1938fb
# 68661508-f3c4-55b4-945d-ae2b4dfe5db4
# 9b9a684f-4201-5785-9966-667603a165cf
