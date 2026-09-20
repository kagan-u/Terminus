const TerminusSimulator = require('../js/terminus');

let passed = 0;
let failed = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`  ✓ ${name}`);
        passed++;
    } catch (e) {
        console.log(`  ✗ ${name}: ${e.message}`);
        failed++;
    }
}

function assert(condition, msg) {
    if (!condition) throw new Error(msg || 'Assertion failed');
}

console.log('\nRunning tests...\n');

test('quadratic model level 0', () => {
    const sim = new TerminusSimulator();
    assert(sim.quadraticModel(0) === 120);
});

test('quadratic model level 50', () => {
    const sim = new TerminusSimulator();
    const size = sim.quadraticModel(50);
    assert(size > 450000 && size < 550000);
});

test('total files formula', () => {
    const sim = new TerminusSimulator(16, 10, 43);
    const result = sim.simulate();
    assert(result.results.totalFiles === Math.pow(16, 10));
});

test('total bytes formula', () => {
    const sim = new TerminusSimulator(8, 5, 100);
    const result = sim.simulate();
    assert(result.results.totalBytes === Math.pow(8, 5) * 100);
});

test('fmtIEC bytes', () => {
    assert(TerminusSimulator.fmtIEC(0) === '0 B');
    assert(TerminusSimulator.fmtIEC(100) === '100.00 B');
});

test('fmtIEC KiB', () => {
    const result = TerminusSimulator.fmtIEC(2048);
    assert(result.includes('KiB'));
});

test('sci notation', () => {
    const result = TerminusSimulator.sci(1000);
    assert(result.includes('e+'));
});

console.log(`\n${passed} passed, ${failed} failed\n`);
process.exit(failed > 0 ? 1 : 0);
