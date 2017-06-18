#!/bin/bash
#
# A script to reset the svm-vs process on the vs computer in the OTB.
#
# Val Schmidt
# CCOM/JHC

echo -e ""
echo -e "RESETTING VS. PLEASE ENTER UNMANNED PASSWORD (UNMANNED:"
ssh -t unmanned@vsc 'sudo systemctl restart scm-vs'
echo -e ""
echo -e "RESET COMPLETE. NOW PLEASE RECONNECT ASVIEW-BRIDGE"
