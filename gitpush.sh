#!/bin/bash

# Script per automatizzare git add, commit e push con pull automatico

echo "=== Git Auto Commit & Push ==="
echo ""

# Ottieni il branch corrente
current_branch=$(git branch --show-current)

# Git add di tutti i file
echo "📦 Aggiungendo tutti i file..."
git add .

# Verifica se ci sono modifiche da committare
if git diff --cached --quiet; then
    echo "❌ Nessuna modifica da committare!"
    exit 0
fi

# Richiedi il messaggio di commit
echo ""
echo "✍️  Inserisci il messaggio del commit:"
read commit_message

# Verifica che il messaggio non sia vuoto
if [ -z "$commit_message" ]; then
    echo "❌ Errore: il messaggio del commit non può essere vuoto!"
    exit 1
fi

# Esegui il commit
echo ""
echo "💾 Eseguendo commit..."
git commit -m "$commit_message"

# Prova a fare push
echo ""
echo "🚀 Pushing su origin $current_branch..."

if git push origin "$current_branch" 2>/dev/null; then
    # Push riuscito
    echo ""
    echo "✅ Commit e push completati con successo!"
else
    # Push fallito, probabilmente serve un pull
    echo ""
    echo "⚠️  Push respinto! Il branch remoto ha nuovi commit."
    echo "🔄 Eseguendo pull con rebase..."
    
    if git pull --rebase origin "$current_branch"; then
        echo ""
        echo "✅ Pull completato! Riprovando il push..."
        
        if git push origin "$current_branch"; then
            echo ""
            echo "✅ Commit e push completati con successo!"
        else
            echo ""
            echo "❌ Errore durante il push dopo il pull!"
            echo "💡 Controlla manualmente lo stato con: git status"
            exit 1
        fi
    else
        echo ""
        echo "❌ Errore durante il pull! Potrebbero esserci conflitti."
        echo "💡 Risolvi i conflitti manualmente e poi esegui:"
        echo "   git rebase --continue"
        echo "   git push origin $current_branch"
        exit 1
    fi
fi
