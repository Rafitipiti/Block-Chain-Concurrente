// eslint-disable-next-line no-promise-executor-return
const delay = async (ms: number) => new Promise((res) => setTimeout(res, ms));

export default delay;
