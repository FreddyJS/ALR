import { applyMiddleware, compose, createStore, combineReducers } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import thunkMiddleware from 'redux-thunk'

import monitorReducersEnhancer from './enhancers/monitorReducer'
import loggerMiddleware from './middleware/logger'

import counterReducer from './reducers/counterReducer'

const rootReducer = combineReducers({
  counter: counterReducer,
})

export default function configureStore(preloadedState) {
  const middlewares = [loggerMiddleware, thunkMiddleware]
  const middlewareEnhancer = applyMiddleware(...middlewares)

  const enhancers = [middlewareEnhancer, monitorReducersEnhancer]

  let composedEnhancers = null
  if (process.env.NODE_ENV === 'development') {
    composedEnhancers = composeWithDevTools(...enhancers)
  } else {
    composedEnhancers = compose(...enhancers)
  }

  const store = createStore(rootReducer, preloadedState, composedEnhancers)
  
  if (process.env.NODE_ENV === 'development' && module.hot) {
    module.hot.accept(rootReducer, () => store.replaceReducer(rootReducer))
  }

  return store
}