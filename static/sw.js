// Service Worker for 五代十国 PWA
const CACHE_NAME = 'wudai-cache-v1';
const urlsToCache = [
  '/',
  '/static/manifest.json',
];

// 安装事件
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

// 激活事件
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// .fetch 事件 - 网络优先，离线时回退到缓存
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 克隆响应以便缓存
        const responseToCache = response.clone();
        caches.open(CACHE_NAME)
          .then(cache => {
            cache.put(event.request, responseToCache);
          });
        return response;
      })
      .catch(() => {
        // 网络失败时从缓存读取
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // 如果是导航请求，返回离线页面
            if (event.request.mode === 'navigate') {
              return caches.match('/');
            }
          });
      })
  );
});

// 后台同步
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(
      // 在这里处理数据同步逻辑
      Promise.resolve()
    );
  }
});

// 推送通知
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || '五代十国';
  const options = {
    body: data.body || '有新的历史数据更新',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
