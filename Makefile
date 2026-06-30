.PHONY: clean build

# Remove build artifacts so stale modules can't leak into the wheel.
clean:
	rm -rf build dist *.egg-info datamaxi.egg-info

# Always build from a clean tree (matches the fresh-checkout CI build).
build: clean
	python -m build
