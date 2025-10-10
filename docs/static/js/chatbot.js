(function() {
    var script = document.createElement("script");
    script.src = "https://pagebotai.lisekarimi.com/static/embed.js";
    script.onload = function() {
        initializePageBotAI({
            chatbotName: 'DatagenBot',
            primaryColor: '#f7323f ',
            instructions: 'You are a helpful AI assistant that answers questions based on the content of the websites you can access. Be friendly, concise, and accurate in your responses. When mentioning documentation pages, always include the hash (#) in URLs, for example: https://datagen.lisekarimi.com/docs/#/development',
            targetUrls: ['https://datagen.lisekarimi.com/docs'],
            wsUrl: 'https://pagebotai.lisekarimi.com/ws/chat'
        });
    };
    document.head.appendChild(script);
})();
