all: clean

clean:
	@rm */*/*.out 2> /dev/null || true
	@rm -rf */__pycache__ 2> /dev/null || true
