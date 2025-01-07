const _p = {true: 'r', false: 'w'}
const _s = { 
    true: 'w-100 block p-2 m m-t-b-4 brd-green clr-green bg-white sdw rnd-1',
    false: 'w-100 block p-2 m m-t-b-4 brd-red clr-red bg-white sdw rnd-1'
}
const _m = _ => document.getElementById(_).play();
let _ = -1; let _b = -1;
const ___ = (__) => {
    ++_; 
    if (!_) {
        _m(_p[v[__.id]]);
        __.className = _s[v[__.id]];
        [...__.parentElement.children].forEach(child => {
            if (__.id != child.id && v[child.id]) 
                child.className = _s[v[child.id]]; 
        });
        document.getElementById('c-f').style.display = 'block';
    }
    window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
}
const buddhirKhela = __ => {
    ++_b; if (!_b) fetch(`/amar-onek-buddhi/${__.id}`);
}
