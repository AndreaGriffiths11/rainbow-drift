// Copyright (C) 2026 Andrea Liliana Griffiths; SPDX-License-Identifier: AGPL-3.0-only
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('./game/index.html',import.meta.url),'utf8');
const body=source.match(/function edge\([^}]+}/)?.[0];
assert.ok(body,'edge function missing');
const edge=vm.runInNewContext(`${body};edge`,{Math});
const radius=([x,y])=>Math.hypot(x/300,y/205);

assert.equal(JSON.stringify(edge(300,0)),JSON.stringify([300,0,false]));
assert.ok(Math.abs(radius(edge(600,0))-1.27)<1e-12);
assert.ok(Math.abs(radius(edge(30,0))-.73)<1e-12);
assert.ok(Math.abs(radius(edge(0,0))-.73)<1e-12);
for(const point of [[-900,80],[40,-500],[-20,10],[210,150]]){
  const r=radius(edge(...point));
  assert.ok(r>=.73-1e-12&&r<=1.27+1e-12,`${point} escaped at ${r}`);
}
console.log('guardrail geometry: ok');
