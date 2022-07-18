FROM node:latest

WORKDIR /opt/app

COPY app/ /opt/app

ENV NODE_ENV production


RUN npm ci 

RUN npm install --dev && npm run build

EXPOSE 3000

CMD [ "npm", "start" ]