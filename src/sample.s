	.att_syntax
	.text
	.p2align	5
	.global	_sample_f
_sample_f:
	movq	%rdi, %r9
	movq	$0, %rax
	movq	$0, %rdi
	movq	$1, %rdx
	movq	$1, %r8
	movq	%rax, %rcx
	imulq	$8, %rcx, %rcx
	addq	%rsi, %rcx
	movq	(%rcx), %rcx
	andq	%rdx, %rcx
	addq	%rdx, %rdx
	incq	%rdi
	cmpq	$64, %rdi
	jne 	Lsample_f$5
	movq	$0, %rdi
	incq	%rax
	movq	$1, %rdx
Lsample_f$5:
	movq	$1, %r10
	decq	%r9
	jmp 	Lsample_f$1
Lsample_f$2:
	movq	%rax, %r11
	imulq	$8, %r11, %r11
	addq	%rsi, %r11
	movq	(%r11), %r11
	andq	%rdx, %r11
	addq	%rdx, %rdx
	incq	%rdi
	cmpq	$64, %rdi
	jne 	Lsample_f$4
	movq	$0, %rdi
	incq	%rax
	movq	$1, %rdx
Lsample_f$4:
	cmpq	$0, %r11
	je  	Lsample_f$3
	movq	$0, %r8
Lsample_f$3:
	incq	%r10
Lsample_f$1:
	cmpq	%r9, %r10
	jb  	Lsample_f$2
	imulq	$8, %rax, %rax
	addq	%rsi, %rax
	movq	(%rax), %r11
	andq	%rdx, %r11
	addq	%r11, %r11
	decq	%r11
	movq	$1, %rax
	subq	%rcx, %rax
	addq	%r8, %r8
	addq	%r8, %rax
	imulq	%rax, %r11
	movq	%r11, %rax
	ret
	.ident	"Jasmin Compiler 2026.03.0"
