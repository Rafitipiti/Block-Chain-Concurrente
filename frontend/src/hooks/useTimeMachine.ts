import { useEffect, useState } from 'react';

import usePrevious from './usePrevious';

const useTimeMachine = <T>(
  initial: T,
  // eslint-disable-next-line no-unused-vars
): [T, (value: T) => void, () => void, () => void, () => void, () => boolean, () => boolean] => {
  const [history, setHistory] = useState<T[]>([initial]);
  const [currentState, setCurrentState] = useState<T>(initial);
  const prevState = usePrevious<T>(currentState);
  const [index, setIndex] = useState<number>(0);

  useEffect(() => {
    setIndex(history.length - 1);
  }, [history]);

  useEffect(() => {
    setCurrentState(history[index]);
  }, [index]);

  const changeState = (value: T): void => {
    if (index !== history.length - 1) return;
    if (value === history[history.length - 1]) return;
    setHistory([...history, value]);
    setIndex(history.length);
  };

  const resume = () => {
    setIndex(history.length - 1);
  };

  const prev = () => {
    if (index === 0) return;
    setIndex(index - 1);
  };

  const next = () => {
    if (index === history.length - 1) return;
    setIndex(index + 1);
  };

  const atFirst = () => index !== 0;
  const atLast = () => index !== history.length - 1;

  return [currentState, changeState, prev, resume, next, atFirst, atLast];
};

export default useTimeMachine;
