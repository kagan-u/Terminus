/**
 * terminus-sim - JavaScript port of terminus simulator
 */

class TerminusSimulator {
    constructor(branching = 16, level = 50, payload = 43, payloadType = 'zeros') {
        this.branching = Math.min(branching, 1000);
        this.level = Math.min(level, 200);
        this.payload = Math.min(payload, 10000);
        this.payloadType = payloadType;
    }

    quadraticModel(level) {
        const a = 68.5, b = 5850.0, c = 120.0;
        return a * Math.pow(level, 2) + b * level + c;
    }

    simulate() {
        const totalFiles = Math.pow(this.branching, this.level);
        const totalBytes = totalFiles * this.payload;

        const levels = [];
        for (let d = 0; d <= this.level; d++) {
            let zipSize = this.quadraticModel(d);
            zipSize = zipSize * (1 + (this.payload - 43) * 0.001);
            const filesHere = Math.pow(this.branching, d);
            const uncompressed = filesHere * this.payload;
            const ratio = uncompressed / zipSize;

            levels.push({
                depth: d,
                zipSize: zipSize,
                files: filesHere,
                uncompressed: uncompressed,
                ratio: ratio,
            });
        }

        return {
            config: {
                branching: this.branching,
                level: this.level,
                payload: this.payload,
                payloadType: this.payloadType,
            },
            results: {
                totalFiles: totalFiles,
                totalBytes: totalBytes,
                zipSize: levels[levels.length - 1].zipSize,
                ratio: totalBytes / levels[levels.length - 1].zipSize,
            },
            levels: levels,
        };
    }

    static fmtIEC(b) {
        if (b === 0) return "0 B";
        const units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
        let i = 0;
        while (b >= 1024 && i < units.length - 1) {
            b /= 1024;
            i++;
        }
        return `${b.toFixed(2)} ${units[i]}`;
    }

    static sci(n) {
        return n.toExponential(4);
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = TerminusSimulator;
}
