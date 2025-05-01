const TelegramBot = require('node-telegram-bot-api');
const { Configuration, OpenAIApi } = require('openai');

const telegramToken = process.env.TELEGRAM_TOKEN;
const openaiApiKey = process.env.OPENAI_API_KEY;

const bot = new TelegramBot(telegramToken, { polling: true });

const configuration = new Configuration({ apiKey: openaiApiKey });
const openai = new OpenAIApi(configuration);

// Limit konfigurasi
const userQuestions = {};
const MAX_QUESTIONS = 50;
const MAX_TOKENS = 1000;

bot.on('message', async (msg) => {
  try {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    if (!msg.text) {
      bot.sendMessage(chatId, 'Kirim teks ya!');
      return;
    }

    // Cek limit
    if (!userQuestions[userId]) userQuestions[userId] = 0;
    if (userQuestions[userId] >= MAX_QUESTIONS) {
      bot.sendMessage(chatId, '❌ Kamu sudah tanya 50x. Coba lagi besok ya.');
      return;
    }

    userQuestions[userId] += 1;

    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      max_tokens: MAX_TOKENS,
      messages: [{ role: 'user', content: msg.text }],
    });

    const reply = response.data.choices[0].message.content;
    bot.sendMessage(chatId, reply);
  } catch (err) {
    console.error(err);
    if (msg?.chat?.id) bot.sendMessage(msg.chat.id, '⚠️ Maaf, ada error.');
  }
});
