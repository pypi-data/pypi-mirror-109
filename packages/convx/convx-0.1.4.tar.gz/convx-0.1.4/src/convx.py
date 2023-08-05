from riposte import Riposte

calculator = Riposte(prompt="▲:~$ ")

MEMORY = []


def main():
    print(
        r"""
 ________  ________  ________   ___      ___ ___    ___ 
|\   ____\|\   __  \|\   ___  \|\  \    /  /|\  \  /  /|
\ \  \___|\ \  \|\  \ \  \\ \  \ \  \  /  / | \  \/  / /
 \ \  \    \ \  \\\  \ \  \\ \  \ \  \/  / / \ \    / / 
  \ \  \____\ \  \\\  \ \  \\ \  \ \    / /   /     \/  
   \ \_______\ \_______\ \__\\ \__\ \__/ /   /  /\   \  
    \|_______|\|_______|\|__| \|__|\|__|/   /__/ /\ __\ 
                                            |__|/ \|__| 
                                                        
    Type "help" for help.                                                        
    """
    )
    calculator.run()


@calculator.command("dtb")
def decimalToBinary(x: int):
    binary = format(x, "b")
    # binary = "{0:b}".format(int(x))
    result = f"{x} to binary = {binary}"
    MEMORY.append(result)
    calculator.success(result)
    return binary


@calculator.command("btd")
def binaryToDecimal(x: str):
    # i,integer = 0,0
    # size = len(x)
    # while i < len(x):
    #    integer += int(x[size - 1 - i])*pow(2,i)
    #     i+=1
    integer = int(x, 2)
    result = f"{x} to integer = {integer}"
    MEMORY.append(result)
    calculator.success(result)
    return integer


@calculator.command("dth")
def decimalToHex(x: str):
    hex = format(int(x), "X")
    result = f"{x} to hex = {hex}"
    MEMORY.append(result)
    calculator.success(result)
    return hex


@calculator.command("bth")
def binaryToHex(x: str):
    integer = int(x, 2)
    calculator.status("Converting to integer: ", x, "to", integer)
    hex = format(integer, "X")
    result = f"{x} to hex = {hex}"
    MEMORY.append(result)
    calculator.success(result)
    return hex


@calculator.command("dtbcd")
def decimalToBCD(x: int):
    n = x
    bcdList = []
    if n == 0:
        bcd = "0000"
        result = f"{x} to BCD = {bcd}"
        MEMORY.append(result)
        calculator.success(result)
        return bcd
    rev = 0
    while n > 0:
        rev = rev * 10 + (n % 10)
        n = n // 10
    while rev > 0:
        b = str(rev % 10)
        bcdListItem = str("{0:04b}".format(int(b, 16)))
        bcdList.append(bcdListItem)
        rev = rev // 10
    bcd = " ".join(bcdList)
    result = f"{x} to BCD = {bcd}"
    MEMORY.append(result)
    calculator.success(result)
    return bcd


@calculator.command("bcdtd")
def bcdToDecimal(x: str):
    length = len(x)
    check = 0
    check0 = 0
    num = 0
    sum = 0
    mul = 1
    rev = 0
    for i in range(length - 1, -1, -1):
        sum += (ord(x[i]) - ord("0")) * mul
        mul *= 2
        check += 1
        if check == 4 or i == 0:
            if sum == 0 and check0 == 0:
                num = 1
                check0 = 1
            else:
                num = num * 10 + sum
            check = 0
            sum = 0
            mul = 1
    while num > 0:
        rev = rev * 10 + (num % 10)
        num //= 10
    if check0 == 1:
        rev -= 1
    decimal = rev
    result = f"{x} to decimal = {decimal}"
    MEMORY.append(result)
    calculator.success(result)
    return decimal


@calculator.command("add")
def addBinary(x: str, y: str):
    max_len = max(len(x), len(y))
    x = x.zfill(max_len)
    y = y.zfill(max_len)
    calculator.status("Initializing Result")
    result = ""
    calculator.status("Initializing Carry")
    carry = 0
    calculator.status("Traversing String")
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if x[i] == "1" else 0
        r += 1 if y[i] == "1" else 0
        result = ("1" if r % 2 == 1 else "0") + result
        calculator.info("- Result (", i, ") :", result)
        # calculator.info("- [/] Computing Carry")
        carry = 0 if r < 2 else 1
        calculator.info("- Carry :", r)
    if carry != 0:
        calculator.info("- Carry !=0, adding 1 to start of", result)
        result = "1" + result
        cleanReturn = result.zfill(max_len)
    result = f"{x} + {y} = {result.zfill(max_len)}"
    # With Internal Functions
    # sum = bin(int(x, 2) + int(y, 2))
    # print(sum[2:])
    MEMORY.append(result)
    calculator.success(result)
    return cleanReturn


@calculator.command("sub")
def subBinary(x: str, y: str):
    binary = bin(int(x, 2) - int(y, 2))[2:]
    result = f"{x} - {y} = {binary}"
    MEMORY.append(result)
    calculator.success(result)
    return binary


@calculator.command("2dtb")
def twoDenaryToBinary(x: int):
    calculator.status("Checking if Positive or Negative")
    if x >= 0:
        calculator.info("[*] Binary is Positive, using normal conversion process")
        binary = format(x, "b")
    else:
        calculator.info("[*] Binary is Negative, using two's compliment")
        denary = str(x)[1:]
        valueList = list(str(bin(int(denary))[2:]))
        calculator.status("Adding MSB")
        valueList.insert(0, "0")
        valueList = [int(i) for i in valueList]
        calculator.status("Inverting value array (finding one's compliment)")
        for i in range(len(valueList)):
            if valueList[i] == 1:
                valueList[i] = "0"
            elif valueList[i] == 0:
                valueList[i] = "1"
            else:
                calculator.error("Error Inverting Value")
        calculator.info("[*] Joining Array into String")
        binary = "".join(str(element) for element in valueList)
        calculator.info("[*] Converting to binary and adding 1 ... for some reason")
        binary = bin(int(binary, 2) + 1)[2:]

    result = f"{x} to binary = {binary}"
    MEMORY.append(result)
    calculator.success(result)
    return binary


@calculator.command("2btd")
def twoBinaryToDenary(x: str):
    valueList = list(x)
    integer = ""
    calculator.status("Checking MSB")
    if valueList[0] == "0":
        calculator.info("[*] Binary is Positive, using normal conversion process")
        integer = int(x, 2)
    elif valueList[0] == "1":
        calculator.info("[*] Binary is Negative, using two's compliment")
        calculator.status("Inverting value array (finding one's compliment)")
        valueList = [int(i) for i in valueList]
        for i in range(len(valueList)):
            if valueList[i] == 1:
                valueList[i] = "0"
            elif valueList[i] == 0:
                valueList[i] = "1"
            else:
                calculator.error("Error Inverting Value")
        calculator.info(
            "[*] Converting to string, adding '-' and adding 1 ... for some reason."
        )
        binary = "".join(str(element) for element in valueList)
        integer = "-" + str(int(binary, 2) + 1)
    else:
        calculator.error("Invalid Value")
    result = f"{x} to integer = {integer}"
    MEMORY.append(result)
    calculator.success(result)
    return int(integer)


@calculator.command("help")
def help():
    calculator.print(
        """ 
  Commands:
    - Conversions
      - Decimal to Binary : dtb
      - Binary to Decimal : btd
      - Decimal to hex    : dth
      - Binary to hex     : bth
      - Decimal to BCD    : dtbcd
      - BCD to Decimal    : bcdtd

    - Adding Binary
      - Command           : add
      - Usage             : add x y

    - Subtracting Binary
      - Command           : sub
      - Usage             : sub x y

    - Two's complement
      - Decimal to Binary : 2dtb
      - Binary to Decimal : 2btd
    
    - Memory
      - Command           : memory
      - Usage             : memory
      """
    )
    return """ 
  Commands:
    - Conversions
      - Decimal to Binary : dtb
      - Binary to Decimal : btd
      - Decimal to hex    : dth
      - Binary to hex     : bth  
      - Decimal to BCD    : dtbcd
      - BCD to Decimal    : bcdtd

    - Adding Binary
      - Command           : add
      - Usage             : add x y

    - Subtracting Binary
      - Command           : sub
      - Usage             : sub x y

    - Two's complement
      - Decimal to Binary : 2dtb
      - Binary to Decimal : 2btd
    
    - Memory
      - Command           : memory
      - Usage             : memory
      """


@calculator.command("memory")
def memory():
    for entry in MEMORY:
        calculator.print(entry)


@calculator.command("exit")
def close():
    exit()


if __name__ == "__main__":
    main()
