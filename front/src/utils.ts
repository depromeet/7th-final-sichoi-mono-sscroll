export const link = (id: number) => {
  const copyText = (x: string) => {
    const el = document.createElement('textarea');
    el.value = x;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    if (navigator.userAgent.match(/ipad|ipod|iphone/i)) {
      const range = document.createRange();
      range.selectNodeContents(el);
      const sel = window.getSelection();
      if (sel) {
        sel.removeAllRanges();
        sel.addRange(range);
        el.setSelectionRange(0, 999999);
      }
    } else {
      el.select();
    }
    document.execCommand('copy');
    document.body.removeChild(el);
  };
  copyText(window.location.host + '/' + id + '?utm_source=share');
  alert('링크가 복사되었습니다!');
};
