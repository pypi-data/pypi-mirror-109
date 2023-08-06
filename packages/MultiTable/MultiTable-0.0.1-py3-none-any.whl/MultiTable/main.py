import os
while True:
    def clear():
        os.system( 'cls' ) 
    def main():
        try:
            num = int(input("Enter the number : "))
            ti = int(input("How Many Times: "))
            ti = ti+1
            clear()
            if ti >= 10000:
                print("Please Put Less Amount")
                ti = 0
                num = 0
            print("Multiplication Table of: ", num)  
            for i in range(1,ti):
                table = num,'x',i,'=',num*i
                print(num,'x',i,'=',num*i)  

        except:
            print("Please don't enter a string or a special letter.")
            ex = input("Do you want to restart? (y/n) ")
            if ex == "n":
                exit()
                os.system('exit')
            if ex == "y":
                clear()
                main()
    main()

