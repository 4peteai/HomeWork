let sessionId = null;
let isWaitingForResponse = false;

let drawerIdCounter = 0;
let hasShownThoughtLabel = false;
let hasShownHeardLabel = false;
let messageCount = 0;
let currentGoal = '';

function updateInputPlaceholder() {
    const input = document.getElementById('user-input');
    if (messageCount === 0 && currentGoal) {
        input.placeholder = currentGoal + '...';
    } else {
        input.placeholder = 'Continue the conversation...';
    }
}

function updateProgress(score) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    
    progressFill.style.width = score + '%';
    progressPercentage.textContent = score + '%';
    
    if (score >= 75) {
        progressFill.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
    } else if (score >= 50) {
        progressFill.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    } else if (score >= 25) {
        progressFill.style.background = 'linear-gradient(135deg, #FF9800 0%, #F57C00 100%)';
    } else {
        progressFill.style.background = 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
    }
}

function addContextCard(contextText) {
    const timeline = document.getElementById('chat-timeline');
    
    const contextCard = document.createElement('div');
    contextCard.className = 'context-card';
    
    const label = document.createElement('div');
    label.className = 'context-label';
    label.textContent = 'CONTEXT';
    
    const content = document.createElement('div');
    content.className = 'context-content';
    content.textContent = contextText;
    
    contextCard.appendChild(label);
    contextCard.appendChild(content);
    timeline.appendChild(contextCard);
}

async function loadPersona() {
    try {
        const response = await fetch('/persona');
        const data = await response.json();
        console.log('Persona loaded:', data);
        
        sessionId = data.session_id;
        console.log('Session initialized:', sessionId);
        
        currentGoal = data.goal;
        
        addContextCard('You sent a calendar invite to discuss a scope change for Jira tickets.');
        
        const openingMsg = data.opening_message;
        addAlexMessageCard(openingMsg.alex_spoken_response, openingMsg.alex_inner_thought);
        
        updateInputPlaceholder();
    } catch (error) {
        console.error('Error loading persona:', error);
        alert('Failed to load scenario. Please refresh the page.');
    }
}

function showInsightTooltip(event, text) {
    let tooltip = document.getElementById('insight-tooltip');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.id = 'insight-tooltip';
        tooltip.className = 'insight-tooltip';
        document.body.appendChild(tooltip);
        
        tooltip.addEventListener('click', function() {
            hideInsightTooltip();
        });
    }
    
    tooltip.innerHTML = text;
    tooltip.style.display = 'block';
    
    if (window.innerWidth <= 768) {
        tooltip.style.left = '0';
        tooltip.style.top = '0';
    } else {
        const iconRect = event.target.getBoundingClientRect();
        const tooltipWidth = 250;
        tooltip.style.left = (iconRect.left + iconRect.width / 2 - tooltipWidth / 2) + 'px';
        tooltip.style.top = (iconRect.top - tooltip.offsetHeight - 10) + 'px';
    }
}

function hideInsightTooltip() {
    const tooltip = document.getElementById('insight-tooltip');
    if (tooltip) {
        tooltip.style.display = 'none';
    }
}

function toggleInsightTooltip(event, text) {
    const tooltip = document.getElementById('insight-tooltip');
    if (tooltip && tooltip.style.display === 'block') {
        hideInsightTooltip();
    } else {
        showInsightTooltip(event, text);
    }
}

function addUserMessageCard(text, perception = null, coachingTip = null, directorWarning = '') {
    const timeline = document.getElementById('chat-timeline');
    
    const turn = document.createElement('div');
    turn.className = 'message-turn user-turn';
    
    if (coachingTip) {
        const insightIcon = document.createElement('div');
        insightIcon.className = 'insight-icon';
        insightIcon.textContent = '💡';
        const tooltipContent = directorWarning ? directorWarning + '<br><br>' + coachingTip : coachingTip;
        insightIcon.onmouseenter = (e) => showInsightTooltip(e, tooltipContent);
        insightIcon.onmouseleave = hideInsightTooltip;
        insightIcon.onclick = (e) => toggleInsightTooltip(e, tooltipContent);
        turn.appendChild(insightIcon);
    }
    
    const bubble = document.createElement('div');
    bubble.className = 'composite-bubble user-bubble';
    
    const primaryText = document.createElement('div');
    primaryText.className = 'primary-text';
    primaryText.textContent = text;
    bubble.appendChild(primaryText);
    
    if (perception) {
        const whisperText = document.createElement('div');
        whisperText.className = 'whisper-text';
        const label = hasShownHeardLabel ? '👂' : '👂 Alex heard';
        whisperText.innerHTML = `<span class="whisper-icon">${label}</span> ${perception}`;
        bubble.appendChild(whisperText);
        hasShownHeardLabel = true;
    }
    
    turn.appendChild(bubble);
    timeline.appendChild(turn);
    
    return turn;
}

function addAlexMessageCard(text, innerThought = null) {
    const timeline = document.getElementById('chat-timeline');
    
    const turn = document.createElement('div');
    turn.className = 'message-turn alex-turn';
    
    const avatar = document.createElement('div');
    avatar.className = 'alex-avatar';
    avatar.textContent = 'A';
    turn.appendChild(avatar);
    
    const bubble = document.createElement('div');
    bubble.className = 'composite-bubble alex-bubble';
    
    const primaryText = document.createElement('div');
    primaryText.className = 'primary-text';
    primaryText.textContent = text;
    bubble.appendChild(primaryText);
    
    if (innerThought) {
        const whisperText = document.createElement('div');
        whisperText.className = 'whisper-text';
        const label = hasShownThoughtLabel ? '💭' : '💭 Alex thought';
        whisperText.innerHTML = `<span class="whisper-icon">${label}</span> ${innerThought}`;
        bubble.appendChild(whisperText);
        hasShownThoughtLabel = true;
    }
    
    turn.appendChild(bubble);
    timeline.appendChild(turn);
    
    return turn;
}

function showLoading() {
    const timeline = document.getElementById('chat-timeline');
    
    const loadingTurn = document.createElement('div');
    loadingTurn.id = 'loading-indicator';
    loadingTurn.className = 'message-turn alex-turn';
    
    const avatar = document.createElement('div');
    avatar.className = 'alex-avatar';
    avatar.textContent = 'A';
    loadingTurn.appendChild(avatar);
    
    const bubble = document.createElement('div');
    bubble.className = 'composite-bubble alex-bubble';
    bubble.innerHTML = `
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    loadingTurn.appendChild(bubble);
    timeline.appendChild(loadingTurn);
}

function removeLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message || isWaitingForResponse) return;
    
    addUserMessageCard(message);
    input.value = '';
    messageCount++;
    updateInputPlaceholder();
    
    isWaitingForResponse = true;
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    const sendBtnText = sendBtn.querySelector('.send-btn-text');
    if (sendBtnText) {
        sendBtnText.textContent = 'Thinking...';
    } else {
        sendBtn.textContent = 'Thinking...';
    }
    
    showLoading();
    
    setTimeout(() => {
        const timelineContainer = document.querySelector('.timeline-container');
        timelineContainer.scrollTop = timelineContainer.scrollHeight;
    }, 50);
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        console.log('Chat response received:', data);
        
        if (data.error) {
            removeLoading();
            alert('Error: ' + data.error);
            return;
        }
        
        sessionId = data.session_id;
        
        removeLoading();
        
        const timeline = document.getElementById('chat-timeline');
        const userTurns = timeline.querySelectorAll('.user-turn');
        const lastUserTurn = userTurns[userTurns.length - 1];
        
        if (lastUserTurn && data.alex_perception) {
            const bubble = lastUserTurn.querySelector('.composite-bubble');
            const whisperText = document.createElement('div');
            whisperText.className = 'whisper-text fade-in';
            const label = hasShownHeardLabel ? '👂' : '👂 Alex heard';
            whisperText.innerHTML = `<span class="whisper-icon">${label}</span> ${data.alex_perception}`;
            bubble.appendChild(whisperText);
            hasShownHeardLabel = true;
        }
        
        if (lastUserTurn && data.coaching_tip) {
            const insightIcon = document.createElement('div');
            insightIcon.className = 'insight-icon fade-in';
            insightIcon.textContent = '💡';
            const tooltipContent = data.director_warning ? data.director_warning + '<br><br>' + data.coaching_tip : data.coaching_tip;
            insightIcon.onmouseenter = (e) => showInsightTooltip(e, tooltipContent);
            insightIcon.onmouseleave = hideInsightTooltip;
            insightIcon.onclick = (e) => toggleInsightTooltip(e, tooltipContent);
            lastUserTurn.insertBefore(insightIcon, lastUserTurn.firstChild);
        }
        
        addAlexMessageCard(data.alex_spoken_response, data.alex_inner_thought);
        updateProgress(data.goal_alignment_score || 0);
        
        setTimeout(() => {
            const container = document.querySelector('.timeline-container');
            container.scrollTop = container.scrollHeight;
        }, 100);
        
    } catch (error) {
        removeLoading();
        console.error('Error sending message:', error);
        alert('Failed to send message. Please try again.');
    } finally {
        isWaitingForResponse = false;
        const sendBtn = document.getElementById('send-btn');
        sendBtn.disabled = false;
        const sendBtnText = sendBtn.querySelector('.send-btn-text');
        if (sendBtnText) {
            sendBtnText.textContent = 'Send';
        } else {
            sendBtn.textContent = 'Send';
        }
        input.focus();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('user-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    document.getElementById('scenario-dropdown').addEventListener('change', function(e) {
        console.log('Scenario changed:', e.target.value);
    });

    loadPersona();
});
