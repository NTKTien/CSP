from CSP import parse_equation, solve_csp
def main():
    # Doc du lieu tu ban phim
    equation = input().strip()
    
    # Tach du lieu thanh cac thanh phan
    operands, result, operator = parse_equation(equation)
    
    # Lay ra cac chu cai duy nhat
    letters = set()
    for part in [*operands, result]:
        for char in part:
            if char.isalpha():
                letters.add(char)
            
    # Sap xep theo thu tu alphabet
    letters = sorted(list(letters))
    
    # Danh sach cac chu cai dau
    first_letters = set()
    for operand in operands:
        first_letters.add(operand[0])
    first_letters.add(result[0])
    
    # Tao mien gia tri cho tung chu cai
    domains = {letter: list(range(10)) for letter in letters}
    for letter in first_letters:
        if 0 in domains[letter]:
            domains[letter].remove(0)  # Chu cai dau khong duoc bang 0
    
    # Tao bang gan gia tri
    assignment = {}
    
    # Giai bai toan
    if solve_csp(operands, result, operator, letters, first_letters, domains, assignment):
        # In ket qua theo yeu cau
        print(''.join(str(assignment[letter]) for letter in sorted(assignment.keys())))
    else:
        print("NO SOLUTION")

if __name__ == "__main__":
    main()