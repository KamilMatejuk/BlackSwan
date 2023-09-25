TICKER=BTCUSDT
INTERVAL="1s"

PORT_EMITTER_PRICE=50001
PORT_EMITTER_SINGAL=50002
PORT_TRADING_BOT=50003


# prepare price emitter
dir=emitter_price
cp Dockerfile.template.nest $dir/Dockerfile
echo "PORT=$PORT_EMITTER_PRICE" > $dir/.env.local
echo "{
    \"type\": \"price\",
    \"tokens\": [ \"$TICKER\" ],
    \"intervals\": [ \"$INTERVAL\" ]
}" > $dir/config.json


# prepare signal emitter
dir=emitter_signal
cp Dockerfile.template.nest $dir/Dockerfile
echo "PORT=$PORT_EMITTER_SINGAL" > $dir/.env.local
echo "{
    \"type\": \"signal\",
    \"identifier\": \"manual\",
    \"tokens\": [ \"$TICKER\" ],
    \"chance\": 0 
}" > $dir/config.json


# prepare trade bot
dir=trading_bot
cp Dockerfile.template.nest $dir/Dockerfile
echo "PORT=$PORT_TRADING_BOT"   > $dir/.env.local
echo "BINANCE_USE_TEST=False"   >> $dir/.env.local
echo "BINANCE_API_KEY="         >> $dir/.env.local
echo "BINANCE_API_SECRET="      >> $dir/.env.local
echo "{
    \"minimum_amounts\": {
        \"BTC\": \"0.001\",
        \"USDT\": \"10.0\"
    },
    \"prices\": { \"$TICKER\": $PORT_EMITTER_PRICE },
    \"signals\" : {
        \"manual\": {
            \"port\": $PORT_EMITTER_SINGAL,
            \"tokens\": [\"$TICKER\"]
        }
    }
}" > $dir/config.json


# create docker compose
echo "version: '3'

services:
  emitter_price:
    container_name: emitter_price
    network_mode: host
    build:
      context: "./emitter_price"
    ports:
      - '$PORT_EMITTER_PRICE:$PORT_EMITTER_PRICE'

  emitter_signal:
    container_name: emitter_signal
    network_mode: host
    build:
      context: "./emitter_signal"
    ports:
      - '$PORT_EMITTER_SINGAL:$PORT_EMITTER_SINGAL'

  trading_bot:
    container_name: trading_bot
    network_mode: host
    build:
      context: "./trading_bot"
    ports:
      - '$PORT_TRADING_BOT:$PORT_TRADING_BOT'
    depends_on:
      - emitter_price
      - emitter_signal
" > docker-compose.yml


# start
set -e
docker rm -f emitter_price   2>/dev/null >/dev/null
docker rm -f emitter_signal  2>/dev/null >/dev/null
docker rm -f trading_bot     2>/dev/null >/dev/null

docker compose build
docker compose up



# TODO create signals for tradebot here, not copy it
