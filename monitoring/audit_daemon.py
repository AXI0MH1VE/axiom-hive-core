import asyncio, random, time
from provenance.chain import ProvenanceChain

async def run_continuous_audit():
    chain = ProvenanceChain()
    while True:
        if not chain.records:
            await asyncio.sleep(60); continue
        sample = random.sample(chain.records, min(5, len(chain.records)))
        violations = 0
        for r in sample:
            if not chain.verify_record(r):
                violations += 1
                print("VIOLATION:", r)
        c_value = violations / max(1, len(sample))
        print(f"[{time.strftime('%X')}] Audit C={c_value}")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(run_continuous_audit())