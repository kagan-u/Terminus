const TerminusSimulator = require('../js/terminus');

const sim = new TerminusSimulator(16, 50, 43);
const result = sim.simulate();

console.log('\nTERMINUS JS SIMULATION\n');
console.log(`Branching:  ${result.config.branching}`);
console.log(`Level:      ${result.config.level}`);
console.log(`Payload:    ${result.config.payload} bytes\n`);
console.log(`Total Files: ${TerminusSimulator.sci(result.results.totalFiles)}`);
console.log(`Zip Size:    ${TerminusSimulator.fmtIEC(result.results.zipSize)}`);
console.log(`Output:      ${TerminusSimulator.sci(result.results.totalBytes)} bytes`);
console.log(`Ratio:       1:${TerminusSimulator.sci(result.results.ratio)}\n`);
