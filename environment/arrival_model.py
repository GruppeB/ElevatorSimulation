import random
import numpy as np
import sys


def lagDoc(ankomst, avreise, lunch, lunch_avreise, mellom, etgOversikt):
    ETG = len(etgOversikt)
    startEtg= 1
    inn = 0
    out = 0
    mat = 0
    mat_av = 0
    tur = 0
    lol = True
    test = np.zeros(1)

    etgLunch = np.zeros(ETG)


    while(lol):
        minimal = min(ankomst[inn],avreise[out],mellom[tur], lunch[mat], lunch_avreise[mat_av])

        if(ankomst[inn] == minimal):
            etg = np.random.randint(ETG-1)+2 #Trekker tilfeldig tall mellom 0 og 11, legger så til 2. Alle kommer fra første etasje
            etgOversikt[etg-1] +=1
            print(ankomst[inn], "\t", 1,"\t",etg)
            inn +=1
            #print(etgOversikt)
            if(inn == len(ankomst)):
                inn -= 1
                ankomst[inn] = np.inf

        if(avreise[out] == minimal):
            etg = np.random.randint(ETG-1)+2
            if(etgOversikt[etg-1] > 0):
                etgOversikt[etg-1]= etgOversikt[etg-1] - 1
                #print(avreise[out],"\t",etgOversikt, "\t","Drar!", "\t", etg)
                print(avreise[out], "\t", etg,"\t",1)
                out += 1
                test = np.append(test,etgOversikt[5])
                #print(etgOversikt)
                if(out == len(avreise)):
                    lol = False

        if(lunch[mat] == minimal):
            etg = np.random.randint(ETG-1)+2
            etgLunch[etg-1] +=1
            etgOversikt[etg-1] -= 1
            etgOversikt[0] += 1
            print(lunch[mat], "\t", etg,"\t",1)
            mat += 1
            #print(etgOversikt, "\t", "Lunch! ")
            if(mat == len(lunch)):
                mat -= 1
                lunch[mat] = np.inf


        if(lunch_avreise[mat_av] == minimal):
            etg = np.random.randint(ETG-1)+2
            if(etgLunch[etg-1] > 0):
                etgOversikt[etg-1] += 1
                etgOversikt[0] -= 1
                etgLunch[etg-1] -= 1
                print(lunch_avreise[mat_av], "\t", 1,"\t",etg)
                mat_av += 1
                #print(etgOversikt, "\t" , "TIlbake")
                if(mat_av == len(lunch)):
                    mat_av -= 1
                    lunch_avreise[mat_av] = np.inf

        if(mellom[tur] == minimal):
            etg = np.random.randint(ETG-1)+2
            etg1 = np.random.randint(ETG-1)+2
            if(etg1 != etg):
                etgOversikt[etg-1] -= 1
                etgOversikt[etg1-1] += 1
                print(mellom[tur], "\t", etg, "\t", etg1)
                #print(etgOversikt, "\t", "mellom !!")
                tur += 1
                if(tur == len(mellom)):
                    tur -=1
                    mellom[tur] = 1000000000000000 #np.inf





def main():
    ETG = 13
    N = int(sys.argv[1])
    N_uniform = int(sys.argv[2])
    sigma_ankomst = 2000 #standardavvik
    sigma_avreise = 1600 #standardavvik
    mu_ankomst = 28800 #forventingsverdi

    norm_ankomst = np.zeros(N)
    norm_ankomst = sigma_ankomst * np.random.randn(1,N) + mu_ankomst

    unif_ankomst = np.zeros(N_uniform)
    unif_ankomst = np.random.randint(mu_ankomst/2,mu_ankomst*2, N_uniform)

    ankomst = np.append(norm_ankomst, unif_ankomst)
    ankomst = np.sort(ankomst)

    norm_avreise = np.zeros(N)
    norm_avreise = sigma_ankomst * np.random.randn(1,N) + 2*mu_ankomst

    unif_avreise = np.zeros(N_uniform)
    unif_avreise = np.random.randint(mu_ankomst/8 *15,mu_ankomst/8 * 24, N_uniform)

    avreise = np.append(norm_avreise, unif_avreise)
    avreise = np.sort(avreise)

    N_lunch = int(N*0.4)
    #print(N_lunch)
    lunchtid = mu_ankomst*11.75/8
    sigma_lunch = 10*60 #10 min * 60 sek/min

    lunch = np.zeros(N_lunch)
    lunch = sigma_lunch * np.random.randn(1,N_lunch) + lunchtid
    lunch = np.sort(lunch)

    lunch_avreise = np.zeros(N_lunch)
    lunch_avreise = sigma_lunch * np.random.randn(1,N_lunch) + mu_ankomst*12.25/8
    lunch_avreise = np.sort(lunch_avreise)


    etgOversikt = np.zeros(ETG)


    mellom1 = np.random.randint(mu_ankomst/8 *9,mu_ankomst/8 * 11.5, int(N_lunch/4))
    mellom2 = np.random.randint(mu_ankomst/8 *12.5,mu_ankomst/8 * 15, int(N_lunch/4))
    mellom = np.append(mellom1,mellom2)
    mellom = np.sort(mellom)


    lagDoc(ankomst, avreise, lunch[0], lunch_avreise[0], mellom, etgOversikt)




if __name__ == "__main__":
    main()
