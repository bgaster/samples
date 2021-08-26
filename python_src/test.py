import Sample as S

sample = S.Sample()

resp = sample.query_unread()

# print(resp)

for x in resp:
    print(x)

# sample.delete(3)

# print("after update")

# resp = sample.query_unread()

# # print(resp)

# for x in resp:
#     print(x)
