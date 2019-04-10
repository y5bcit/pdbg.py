@echo off
python -c "import pdbg; pdbg.pdbg('test.py')"
echo Script 1 done
python -c "import pdbg; pdbg.pdbg('func.py')"
echo Script 2 done
python -c "import pdbg; pdbg.pdbg('recu.py')"
echo Script 3 done