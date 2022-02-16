import React from 'react';
import { Button } from 'carbon-components-react';
import { useDispatch, useSelector } from 'react-redux';
import { increment, decrement, incrementByAmount, selectCount, incrementAsync } from '../../reducers/counterReducer';

const CounterPage = () => {
  const dispatch = useDispatch()
  const state = useSelector(state => state)
  const count = useSelector(selectCount);

  return(
    <div className="counter-example">
      <h2>Actual count {count}</h2>
      <p>Actual count from state {state.counter.value}</p>
      <br/>
      <Button onClick={() => dispatch(increment())}>Increment 1</Button>
      <Button onClick={() => dispatch(decrement())}>Decrement 1</Button>
      <Button onClick={() => dispatch(incrementByAmount(2))}>Increment by amount (2)</Button>
      <Button onClick={() => dispatch(incrementAsync(2))}>IncrementAsync by amount (2)</Button>
    </div>
  )
};

export default CounterPage;
