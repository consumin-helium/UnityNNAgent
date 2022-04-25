import time

data_package = {'"up"':'"1"',"timestamp":str(time.time())}
print(data_package)
data_package = str(data_package)


#data_package.replace("'",'"')

data_package.replace("'", '"')

print(data_package);