FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache python3 make g++

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm install react-router-dom tailwind-merge

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
