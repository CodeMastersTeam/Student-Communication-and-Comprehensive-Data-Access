from werkzeug.security import generate_password_hash, check_password_hash


x = generate_password_hash("Password121")

z = "Password121"
c = check_password_hash(x, z)
print(c)