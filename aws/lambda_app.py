from aws.s3_data_fetcher import S3DataFetcher
from common.exam_data_processor import ExamDataProcessor
from common.contracts import read_and_compute
from datetime import datetime
from fetch.api import fetch_stocks
import json
import os

def build_html(stats):

    stocks = fetch_stocks()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇯🇲 Yard Stock Tracker - One Love</title>
    <style>
      * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }}
      
      body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #006b3f 0%, #009b4f 50%, #ffd700 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        position: relative;
      }}
      
      body::before {{
        content: '🌴';
        position: absolute;
        font-size: 120px;
        opacity: 0.1;
        top: 20px;
        left: 50px;
        animation: sway 3s ease-in-out infinite;
      }}
      
      body::after {{
        content: '🌺';
        position: absolute;
        font-size: 80px;
        opacity: 0.15;
        bottom: 40px;
        right: 60px;
        animation: float 4s ease-in-out infinite;
      }}
      
      @keyframes sway {{
        0%, 100% {{ transform: rotate(-5deg); }}
        50% {{ transform: rotate(5deg); }}
      }}
      
      @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-20px); }}
      }}
      
      .container {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 253, 240, 0.95));
        border-radius: 20px;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4), 
                    0 0 0 3px #ffd700,
                    0 0 0 6px #000000,
                    0 0 0 9px #dc143c;
        padding: 45px;
        max-width: 850px;
        width: 100%;
        position: relative;
        z-index: 1;
      }}
      
      .jamaica-stripe {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 8px;
        background: linear-gradient(90deg, 
          #006b3f 0%, #006b3f 33%, 
          #ffd700 33%, #ffd700 66%, 
          #000000 66%, #000000 100%);
        border-radius: 20px 20px 0 0;
      }}
      
      h1 {{
        background: linear-gradient(135deg, #006b3f 0%, #ffd700 50%, #dc143c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8em;
        font-weight: 800;
        margin-bottom: 15px;
        margin-top: 10px;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
      }}
      
      .subtitle {{
        text-align: center;
        color: #006b3f;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 20px;
        font-style: italic;
      }}
      
      .timestamp {{
        text-align: center;
        color: #333;
        font-size: 1em;
        margin-bottom: 30px;
        font-family: 'Courier New', monospace;
        padding: 12px;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        border-radius: 10px;
        display: inline-block;
        width: 100%;
        font-weight: 600;
        border: 2px solid #006b3f;
        box-shadow: 0 4px 12px rgba(0, 107, 63, 0.2);
      }}
      
      table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 25px;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 3px solid #ffd700;
      }}
      
      thead {{
        background: linear-gradient(135deg, #006b3f 0%, #009b4f 100%);
        color: #ffd700;
      }}
      
      th {{
        padding: 18px;
        text-align: left;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.9em;
        letter-spacing: 1.5px;
        border-bottom: 3px solid #ffd700;
      }}
      
      td {{
        padding: 18px;
        border-bottom: 2px solid #ffe680;
        color: #1a1a1a;
        font-weight: 500;
      }}
      
      tbody tr {{
        background: linear-gradient(90deg, #ffffff 0%, #fffef0 100%);
      }}
      
      tbody tr:hover {{
        background: linear-gradient(90deg, #fff9e6 0%, #ffed4e 100%);
        transition: background 0.3s ease;
        transform: scale(1.01);
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
      }}
      
      tbody tr:last-child td {{
        border-bottom: none;
      }}
      
      .ticker {{
        font-weight: 700;
        color: #000000;
        font-family: 'Courier New', monospace;
        font-size: 1.1em;
      }}
      
      .price {{
        font-family: 'Courier New', monospace;
        font-weight: 600;
        color: #006b3f;
        font-size: 1.05em;
      }}
      
      .change {{
        font-weight: 700;
        font-family: 'Courier New', monospace;
        font-size: 1.05em;
      }}
      
      .positive {{
        color: #009b4f;
        text-shadow: 0 0 10px rgba(0, 155, 79, 0.3);
      }}
      
      .negative {{
        color: #dc143c;
        text-shadow: 0 0 10px rgba(220, 20, 60, 0.3);
      }}
      
      .footer {{
        text-align: center;
        margin-top: 25px;
        font-size: 1.2em;
        color: #006b3f;
        font-weight: 600;
      }}
      
      .button-container {{
        display: flex;
        gap: 15px;
        justify-content: center;
        margin: 20px auto;
        flex-wrap: wrap;
      }}
      
      .shuffle-btn, .refresh-btn {{
        padding: 12px 30px;
        font-size: 1.1em;
        font-weight: 700;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #006b3f;
        border: 3px solid #006b3f;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 107, 63, 0.3);
        transition: all 0.3s ease;
      }}
      
      .shuffle-btn:hover, .refresh-btn:hover {{
        background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 107, 63, 0.4);
      }}
      
      .shuffle-btn:active, .refresh-btn:active {{
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(0, 107, 63, 0.3);
      }}
      
      .refresh-btn:disabled {{
        opacity: 0.6;
        cursor: not-allowed;
      }}
      
      .game-container {{
        margin-top: 35px;
        padding: 30px;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 107, 63, 0.1));
        border-radius: 16px;
        border: 3px solid #ffd700;
        box-shadow: 0 4px 15px rgba(0, 107, 63, 0.2);
      }}
      
      .game-container h2 {{
        text-align: center;
        color: #006b3f;
        font-size: 2em;
        margin-bottom: 10px;
      }}
      
      .game-subtitle {{
        text-align: center;
        color: #666;
        font-style: italic;
        margin-bottom: 20px;
      }}
      
      .game-stats {{
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
        gap: 20px;
      }}
      
      .score, .high-score {{
        background: linear-gradient(135deg, #006b3f 0%, #009b4f 100%);
        color: #ffd700;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      }}
      
      #gameArea {{
        position: relative;
        height: 300px;
        background: linear-gradient(180deg, #87CEEB 0%, #98D8C8 100%);
        border-radius: 12px;
        overflow: hidden;
        border: 2px solid #006b3f;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
      }}
      
      #startBtn {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #006b3f;
        border: 3px solid #006b3f;
        padding: 15px 40px;
        font-size: 1.3em;
        font-weight: 700;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        z-index: 100;
      }}
      
      #startBtn:hover {{
        background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%);
        transform: translate(-50%, -50%) scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
      }}
      
      #startBtn:active {{
        transform: translate(-50%, -50%) scale(0.98);
      }}
      
      .fruit {{
        position: absolute;
        top: -50px;
        font-size: 50px;
        cursor: pointer;
        animation: fall 4s linear;
        user-select: none;
        transition: transform 0.1s ease;
      }}
      
      .fruit:hover {{
        transform: scale(1.2) rotate(10deg);
      }}
      
      @keyframes fall {{
        from {{
          top: -50px;
        }}
        to {{
          top: 300px;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="jamaica-stripe"></div>
      <h1>🇯🇲 Yard Stock Tracker 📈</h1>
      <div class="subtitle">One Love, One Market 🌴</div>
      <div class="timestamp" id="timestamp">⏰ {current_time} JA Time</div>
      
      <div class="button-container">
        <button class="shuffle-btn" onclick="shuffleStocks()">🎲 Shuffle Stocks 🎲</button>
        <button class="refresh-btn" id="refreshBtn" onclick="refreshPrices()">🔄 Refresh Prices 🔄</button>
      </div>
      
      <table>
        <thead>
          <tr>
            <th>🎯 Ticker</th>
            <th>💰 Current Price</th>
            <th>📊 Change</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="ticker">{list(stocks.keys())[0]}</td>
            <td class="price">${stocks[list(stocks.keys())[0]]['c']:.2f}</td>
            <td class="change {'positive' if stocks[list(stocks.keys())[0]]['dp'] >= 0 else 'negative'}">
              {'+' if stocks[list(stocks.keys())[0]]['dp'] >= 0 else ''}{stocks[list(stocks.keys())[0]]['dp']:.1f}%
            </td>
          </tr>
          <tr>
            <td class="ticker">{list(stocks.keys())[1]}</td>
            <td class="price">${stocks[list(stocks.keys())[1]]['c']:.2f}</td>
            <td class="change {'positive' if stocks[list(stocks.keys())[1]]['dp'] >= 0 else 'negative'}">
              {'+' if stocks[list(stocks.keys())[1]]['dp'] >= 0 else ''}{stocks[list(stocks.keys())[1]]['dp']:.1f}%
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="game-container">
        <h2>🥭 Tropical Fruit Catch! 🥥</h2>
        <p class="game-subtitle">Click the falling fruits before they hit the ground!</p>
        <div class="game-stats">
          <div class="score">Score: <span id="score">0</span></div>
          <div class="high-score">High Score: <span id="highScore">0</span></div>
        </div>
        <div id="gameArea">
          <button id="startBtn">Start Game</button>
        </div>
      </div>
      
      <div class="footer">Irie Investments 🌺</div>
    </div>
    
    <script>
      // Stock data for randomization
      const allStocks = {json.dumps(stocks)};
      const stockSymbols = Object.keys(allStocks);
      let currentStocks = [stockSymbols[0], stockSymbols[1]];
      const API_KEY = '{os.environ.get("API_KEY", "")}';
      
      function shuffleStocks() {{
        // Select 2 random stocks from the pool
        const shuffled = [...stockSymbols].sort(() => Math.random() - 0.5);
        currentStocks = shuffled.slice(0, 2);
        
        // Update the table
        updateTable();
      }}
      
      function updateTable() {{
        const tbody = document.querySelector('tbody');
        const rows = tbody.querySelectorAll('tr');
        
        currentStocks.forEach((symbol, index) => {{
          const stock = allStocks[symbol];
          const change = stock.dp;
          const changeClass = change >= 0 ? 'positive' : 'negative';
          const changeSign = change >= 0 ? '+' : '';
          
          rows[index].innerHTML = `
            <td class="ticker">${{symbol}}</td>
            <td class="price">$${{stock.c.toFixed(2)}}</td>
            <td class="change ${{changeClass}}">${{changeSign}}${{change.toFixed(1)}}%</td>
          `;
        }});
      }}
      
      async function refreshPrices() {{
        const refreshBtn = document.getElementById('refreshBtn');
        refreshBtn.disabled = true;
        refreshBtn.textContent = '⏳ Updating...';
        
        try {{
          // Fetch fresh data for currently displayed stocks
          for (const symbol of currentStocks) {{
            const response = await fetch(`https://finnhub.io/api/v1/quote?symbol=${{symbol}}&token=${{API_KEY}}`);
            const data = await response.json();
            
            // Update the allStocks data
            allStocks[symbol] = data;
          }}
          
          // Update the table with new data
          updateTable();
          
          // Update timestamp
          const now = new Date();
          const timeString = now.toLocaleString('en-US', {{
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          }}).replace(',', '');
          document.getElementById('timestamp').textContent = `⏰ ${{timeString}} JA Time`;
          
        }} catch (error) {{
          console.error('Error refreshing prices:', error);
          alert('Failed to refresh prices. Please try again.');
        }} finally {{
          refreshBtn.disabled = false;
          refreshBtn.textContent = '🔄 Refresh Prices 🔄';
        }}
      }}
      
      // Minigame code
      const fruits = ['🥭', '🥥', '🍌', '🍍', '🍈', '🍉'];
      let score = 0;
      let highScore = localStorage.getItem('tropicalHighScore') || 0;
      let gameActive = false;
      let gameInterval;
      
      document.getElementById('highScore').textContent = highScore;
      
      document.getElementById('startBtn').addEventListener('click', startGame);
      
      function startGame() {{
        score = 0;
        gameActive = true;
        document.getElementById('score').textContent = score;
        document.getElementById('startBtn').style.display = 'none';
        
        gameInterval = setInterval(createFruit, 1000);
        
        setTimeout(() => {{
          endGame();
        }}, 20000); // 20 second game
      }}
      
      function createFruit() {{
        if (!gameActive) return;
        
        const fruit = document.createElement('div');
        fruit.className = 'fruit';
        fruit.textContent = fruits[Math.floor(Math.random() * fruits.length)];
        fruit.style.left = Math.random() * (document.getElementById('gameArea').offsetWidth - 50) + 'px';
        
        fruit.addEventListener('click', () => {{
          if (gameActive) {{
            score += 10;
            document.getElementById('score').textContent = score;
            fruit.remove();
          }}
        }});
        
        document.getElementById('gameArea').appendChild(fruit);
        
        setTimeout(() => {{
          if (fruit.parentNode) {{
            fruit.remove();
          }}
        }}, 4000);
      }}
      
      function endGame() {{
        gameActive = false;
        clearInterval(gameInterval);
        
        if (score > highScore) {{
          highScore = score;
          localStorage.setItem('tropicalHighScore', highScore);
          document.getElementById('highScore').textContent = highScore;
        }}
        
        document.getElementById('startBtn').textContent = 'Play Again';
        document.getElementById('startBtn').style.display = 'block';
        
        // Clear remaining fruits
        document.querySelectorAll('.fruit').forEach(f => f.remove());
      }}
    </script>
  </body>
</html>
"""

def lambda_handler(event, context):
    print("Starting lambda!")

    result = read_and_compute(
        S3DataFetcher("bulead2026-exam-scores", "test_scores.csv"),
        ExamDataProcessor()
    )

    print(result)

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "text/html; charset=utf-8"},
        'body': build_html(result)
    }