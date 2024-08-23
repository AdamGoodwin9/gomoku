# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default target
all: run

# Create and activate virtual environment
$(VENV)/bin/activate: $(VENV)/pyvenv.cfg
	@echo "Virtual environment already exists."

$(VENV)/pyvenv.cfg:
	python3 -m venv $(VENV)

# Install required packages
install: $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

# Run the program
run: $(VENV)/bin/activate
	$(PYTHON) src/game.py

# Clean the virtual environment
clean:
	rm -rf $(VENV)

# Force clean and reinstall everything
fclean: clean
	$(MAKE) install

# Rebuild everything
re: fclean all

.PHONY: all clean fclean re