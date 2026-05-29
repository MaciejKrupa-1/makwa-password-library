import Makwa,time

"""
Additional module, used in presentation (comparing 2 versions)
"""

p = 134589027020174523962374866939701794935087928680450715947049475548655906267610263109307873581357939084741919190191012616011022073334462546156417229423606540342770954631380491333669236828392871689564309147523844866411345984635020155349344365503362334809704735559325582685954360688611870562923770339712149850963 # 1 liczba piersza
q = 176329745186020171074354648217969201729310872760817531156579638907145323489384602975233683278624696384573257044806950800200208801892028561827612286660256097328319716195813017092756054974428925237872354721906623425043814666723134362527454116132923680731699242547255648291685754535330509293538091678957710515223 # 2 liczba pierwsza
print(Makwa.checkIsBlumNumber(p,q))
preHashing = False
postHashing = 20
N = p*q
hashesNormal = []
salts = []
hashesQuick = []
mcost = 4096
salt = Makwa.generate_salt()

#'''
start_quick = time.time()
with open('passwords.txt', 'r', encoding='utf-8') as f:
    for linia in f:
        salt = Makwa.generate_salt()
        salts.append(salt)
        hashesQuick.append(Makwa.makwa_hash(linia,salt,mcost,postHashing,preHashing,N,p,q))
with open('hashesQuick.txt', 'w', encoding='utf-8') as f:
    for hash in hashesQuick:
        f.write(str(hash))
        f.write('\n')
end_quick = time.time()
print(f'czas hashowania ze znajomością rozkładu {end_quick-start_quick}')
start_normal = time.time()
with open('passwords.txt', 'r', encoding='utf-8') as f:
    i = 0
    for linia in f:
        salt = salts[i]
        i += 1
        hashesNormal.append(Makwa.makwa_hash(linia,salt,mcost,postHashing,preHashing,N))

with open('hashesNormal.txt', 'w', encoding='utf-8') as f:
    for hash in hashesNormal:
        f.write(str(hash))
        f.write('\n')
end_normal = time.time()
print(f'czas bez znajomości rozkładu {end_normal-start_normal}')