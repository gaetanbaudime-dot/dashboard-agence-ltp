#!/bin/bash
curl -sL "https://raw.githubusercontent.com/gaetanbaudime-dot/dashboard-agence-ltp/claude/tikfusion-setup-sharing-LX55Z/tikfusion-update/app.py" -o app.py
curl -sL "https://raw.githubusercontent.com/gaetanbaudime-dot/dashboard-agence-ltp/claude/tikfusion-setup-sharing-LX55Z/tikfusion-update/requirements.txt" -o requirements.txt
git add -A && git commit -m "v4" && git push
echo "✅ Déployé! Refresh tikfusion.streamlit.app"
