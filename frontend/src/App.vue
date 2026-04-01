<script setup>
import { ref, computed } from 'vue'
import { marked } from 'marked'

const activeTab = ref('meeting') // 'meeting', 'document', 'scheduling', 'translation'

// Meeting Logic
const transcript = ref('')
const summary = ref('')
const meetingLoading = ref(false)

const generateSummary = async () => {
  if (!transcript.value) return
  meetingLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/meeting/summary', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ transcript: transcript.value }),
    })
    const data = await response.json()
    summary.value = data.summary
  } catch (error) {
    console.error('Error:', error)
    alert('生成摘要失败。')
  } finally {
    meetingLoading.value = false
  }
}

// Document Logic
const docText = ref('')
const question = ref('')
const answer = ref('')
const docLoading = ref(false)
const ingestStatus = ref('')

const ingestDoc = async () => {
  if (!docText.value) return
  docLoading.value = true
  try {
    await fetch(`http://localhost:8000/api/v1/document/ingest?text=${encodeURIComponent(docText.value)}`, { method: 'POST' })
    ingestStatus.value = '文档解析成功！'
  } catch (error) {
    alert('文档解析失败。')
  } finally {
    docLoading.value = false
  }
}

const queryDoc = async () => {
  if (!question.value) return
  docLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/document/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question.value }),
    })
    const data = await response.json()
    answer.value = data.answer
  } catch (error) {
    alert('问答失败。')
  } finally {
    docLoading.value = false
  }
}

// Scheduling Logic
const scheduleText = ref('')
const parsedSchedule = ref(null)
const scheduleLoading = ref(false)

const parseSchedule = async () => {
  if (!scheduleText.value) return
  scheduleLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/scheduling/parse', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: scheduleText.value }),
    })
    const data = await response.json()
    parsedSchedule.value = typeof data.schedule === 'string' ? JSON.parse(data.schedule) : data.schedule
  } catch (error) {
    alert('排程解析失败。')
  } finally {
    scheduleLoading.value = false
  }
}

// Translation Logic
const sourceText = ref('')
const targetLang = ref('中文')
const translatedResult = ref('')
const transLoading = ref(false)

// Markdown rendering
const renderedSummary = computed(() => marked.parse(summary.value || ''))
const renderedAnswer = computed(() => marked.parse(answer.value || ''))
const renderedTranslatedResult = computed(() => marked.parse(translatedResult.value || ''))

const translateText = async () => {
  if (!sourceText.value) return
  transLoading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/v1/translation/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: sourceText.value, target_lang: targetLang.value }),
    })
    const data = await response.json()
    translatedResult.value = data.translated_text
  } catch (error) {
    alert('翻译失败。')
  } finally {
    transLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen p-8 bg-background">
    <header class="mb-12 max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center md:items-end gap-6">
      <div>
        <h1 class="text-4xl font-bold mb-2 tracking-tight text-text">Smart Office Assistant</h1>
        <p class="text-slate-400">你的智能办公效率管家</p>
      </div>
      <nav class="flex flex-wrap gap-2 bg-primary p-1.5 rounded-xl border border-slate-700/50 shadow-2xl">
        <button v-for="tab in ['meeting', 'document', 'scheduling', 'translation']" :key="tab"
          @click="activeTab = tab"
          :class="['px-4 py-2 rounded-lg transition-all text-sm font-medium',
            activeTab === tab ? 'bg-cta text-white shadow-lg' : 'text-slate-400 hover:text-text hover:bg-slate-800']"
        >
          {{ {meeting:'会议助手', document:'文档分析', scheduling:'智能排程', translation:'极简翻译'}[tab] }}
        </button>
      </nav>
    </header>

    <main class="max-w-6xl mx-auto">
      <!-- 会议助手 -->
      <div v-if="activeTab === 'meeting'" class="space-y-8 animate-in fade-in duration-300">
        <section class="bg-primary p-8 rounded-2xl shadow-xl border border-slate-700/50">
          <h2 class="text-xl font-bold mb-6 flex items-center gap-3">
            <span class="p-2 bg-cta/10 rounded-lg text-cta"><svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg></span>
            会议记录输入
          </h2>
          <textarea v-model="transcript" class="w-full h-64 bg-background border border-slate-700 rounded-xl p-6 text-text focus:outline-none focus:ring-2 focus:ring-cta transition-all text-lg" placeholder="在此粘贴会议实时转写的文字内容..."></textarea>
          <div class="mt-6 flex justify-end">
            <button @click="generateSummary" :disabled="meetingLoading || !transcript" class="btn-primary">
              {{ meetingLoading ? '分析中...' : '生成摘要' }}
            </button>
          </div>
        </section>
        <section v-if="summary" class="bg-primary p-8 rounded-2xl shadow-xl border border-slate-700/50">
          <h2 class="text-xl font-bold mb-6 text-cta">会议总结</h2>
          <div class="markdown-content text-slate-300 text-lg leading-relaxed" v-html="renderedSummary"></div>
        </section>
      </div>

      <!-- 文档分析 -->
      <div v-if="activeTab === 'document'" class="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in">
        <section class="bg-primary p-8 rounded-2xl border border-slate-700/50">
          <h2 class="text-xl font-bold mb-6 text-text">上传文档文本</h2>
          <textarea v-model="docText" class="w-full h-96 bg-background border border-slate-700 rounded-xl p-4 text-text" placeholder="粘贴长文..."></textarea>
          <button @click="ingestDoc" :disabled="docLoading || !docText" class="btn-primary w-full mt-4">解析文档</button>
          <p v-if="ingestStatus" class="mt-2 text-cta text-center">{{ ingestStatus }}</p>
        </section>
        <section class="space-y-8">
          <div class="bg-primary p-8 rounded-2xl border border-slate-700/50">
            <h2 class="text-xl font-bold mb-6">提问 AI</h2>
            <input v-model="question" class="w-full bg-background border border-slate-700 rounded-xl px-4 py-3 mb-4" placeholder="问点什么..." @keyup.enter="queryDoc" />
            <button @click="queryDoc" :disabled="docLoading || !question" class="btn-primary w-full">查询</button>
          </div>
          <div v-if="answer" class="bg-primary p-8 rounded-2xl border border-slate-700/50 min-h-[200px]">
            <h3 class="text-cta font-bold mb-4">回答：</h3>
            <div class="markdown-content text-slate-300" v-html="renderedAnswer"></div>
          </div>
        </section>
      </div>

      <!-- 智能排程 -->
      <div v-if="activeTab === 'scheduling'" class="max-w-3xl mx-auto space-y-8 animate-in fade-in">
        <section class="bg-primary p-8 rounded-2xl border border-slate-700/50">
          <h2 class="text-xl font-bold mb-6 text-text">语音/文本约会</h2>
          <input v-model="scheduleText" class="w-full bg-background border border-slate-700 rounded-xl px-4 py-4 text-lg mb-4" placeholder="例：帮我约明天下午两点和张三开需求评审会" @keyup.enter="parseSchedule" />
          <button @click="parseSchedule" :disabled="scheduleLoading || !scheduleText" class="btn-primary w-full">解析意图</button>
        </section>
        <section v-if="parsedSchedule" class="bg-primary p-8 rounded-2xl border border-slate-700/50">
          <h2 class="text-xl font-bold mb-4 text-cta">解析结果</h2>
          <div class="grid grid-cols-2 gap-4 text-slate-300">
            <div class="bg-background p-4 rounded-xl"><p class="text-xs text-slate-500">主题</p><p class="font-bold">{{ parsedSchedule.subject || '-' }}</p></div>
            <div class="bg-background p-4 rounded-xl"><p class="text-xs text-slate-500">时间</p><p class="font-bold">{{ parsedSchedule.start_time || '-' }}</p></div>
            <div class="bg-background p-4 rounded-xl"><p class="text-xs text-slate-500">人员</p><p class="font-bold">{{ parsedSchedule.participants?.join(', ') || '-' }}</p></div>
            <div class="bg-background p-4 rounded-xl"><p class="text-xs text-slate-500">时长</p><p class="font-bold">{{ parsedSchedule.duration_minutes || '-' }} 分钟</p></div>
          </div>
        </section>
      </div>

      <!-- 极简翻译 -->
      <div v-if="activeTab === 'translation'" class="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-in fade-in">
        <section class="bg-primary p-8 rounded-2xl border border-slate-700/50">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold">原文</h2>
            <select v-model="targetLang" class="bg-background border border-slate-700 rounded-lg px-3 py-1 text-sm">
              <option>中文</option><option>English</option><option>日本語</option>
            </select>
          </div>
          <textarea v-model="sourceText" class="w-full h-80 bg-background border border-slate-700 rounded-xl p-4" placeholder="输入要翻译的文本..."></textarea>
          <button @click="translateText" :disabled="transLoading || !sourceText" class="btn-primary w-full mt-4">开始翻译</button>
        </section>
        <section class="bg-primary p-8 rounded-2xl border border-slate-700/50 min-h-[400px]">
          <h2 class="text-xl font-bold mb-6 text-cta">译文</h2>
          <div class="markdown-content text-lg text-slate-300 leading-relaxed" v-html="renderedTranslatedResult || '等待翻译...'"></div>
        </section>
      </div>
    </main>
  </div>
</template>

<style>
@reference "./style.css";
.btn-primary {
  @apply bg-cta text-white px-8 py-3 rounded-xl font-bold hover:bg-green-600 hover:shadow-[0_0_20px_rgba(34,197,94,0.3)] active:scale-95 cursor-pointer disabled:opacity-40 transition-all duration-300;
}

.markdown-content h1 {
  @apply text-2xl font-bold mb-4 mt-2;
}
.markdown-content h2 {
  @apply text-xl font-bold mb-3 mt-2;
}
.markdown-content h3 {
  @apply text-lg font-bold mb-2 mt-1;
}
.markdown-content p {
  @apply mb-4;
}
.markdown-content ul {
  @apply list-disc list-inside mb-4;
}
.markdown-content ol {
  @apply list-decimal list-inside mb-4;
}
.markdown-content li {
  @apply mb-1;
}
.markdown-content code {
  @apply bg-slate-800 px-1.5 py-0.5 rounded text-sm font-mono;
}
.markdown-content pre {
  @apply bg-slate-800 p-4 rounded-xl mb-4 overflow-x-auto;
}
.markdown-content pre code {
  @apply bg-transparent p-0;
}
.markdown-content blockquote {
  @apply border-l-4 border-slate-600 pl-4 italic mb-4;
}
</style>
