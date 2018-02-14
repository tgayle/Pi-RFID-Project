import Script

print("What kind of script would you like to create?")

for i,k in enumerate(Script.TYPES):
    print("%s: %s" % (i, k))

selected_option = int(input())
while selected_option not in range(len(range(Script.TYPES))):
