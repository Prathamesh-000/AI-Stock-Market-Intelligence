import { Prediction, Timeframe, ChartDataResult, ChartPoint } from '../types';

export function generateChartData(
  pred: Prediction,
  tf: Timeframe = '1D',
  livePrice?: number
): ChartDataResult {
  const currentPrice = livePrice && livePrice > 0 ? livePrice : (pred.current_price || 200.0);
  const eventTimeStr = new Date(pred.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const data: ChartPoint[] = [];

  if (tf === '1D') {
    const predMove = pred.pred_1h || 0.16;
    let base = currentPrice - (predMove / 10 * 50);
    for (let i = 0; i < 50; i++) {
      base = base + (Math.random() - 0.45) * 0.4;
      data.push({ time: i === 0 ? "9:30 AM" : i === 25 ? "12:00 PM" : '', price: Number(base.toFixed(2)) });
    }
    for (let i = 50; i < 60; i++) {
      base = base + (predMove / 10) + (Math.random() - 0.5) * 0.2;
      data.push({ time: i === 50 ? eventTimeStr : i === 59 ? "+1H" : '', price: Number(base.toFixed(2)) });
    }
    const startPrice = data[0].price;
    const endPrice = data[data.length - 1].price;
    const delta = Number((endPrice - startPrice).toFixed(2));
    const changePct = Number(((delta / startPrice) * 100).toFixed(2));
    return { data, eventMarker: eventTimeStr, changePct, delta, currentPrice: endPrice, periodLabel: 'Today' };
  }

  if (tf === '1W') {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
    const weeklyReturnPct = Number(((pred.pred_1h || 0.2) * 2.5 + 1.2).toFixed(2));
    let base = currentPrice / (1 + weeklyReturnPct / 100);
    for (let d = 0; d < 4; d++) {
      for (let h = 0; h < 6; h++) {
        base = base + (Math.random() - 0.47) * (currentPrice * 0.005);
        data.push({ time: h === 0 ? days[d] : '', price: Number(base.toFixed(2)) });
      }
    }
    for (let h = 0; h < 6; h++) {
      base = base + ((currentPrice - base) / (6 - h)) + (Math.random() - 0.5) * 0.5;
      data.push({ time: h === 2 ? 'EVENT' : h === 5 ? 'Fri' : '', price: Number(base.toFixed(2)) });
    }
    const startPrice = data[0].price;
    const endPrice = data[data.length - 1].price;
    const delta = Number((endPrice - startPrice).toFixed(2));
    const changePct = Number(((delta / startPrice) * 100).toFixed(2));
    return { data, eventMarker: 'EVENT', changePct, delta, currentPrice: endPrice, periodLabel: 'Past Week' };
  }

  // 1M (1 Month)
  const monthlyReturnPct = Number(((pred.pred_1h || 0.2) * 6.0 + 4.5).toFixed(2));
  let base = currentPrice / (1 + monthlyReturnPct / 100);
  const weeks = ['Wk 1', 'Wk 2', 'Wk 3', 'Wk 4'];
  for (let w = 0; w < 3; w++) {
    for (let d = 0; d < 5; d++) {
      base = base + (Math.random() - 0.46) * (currentPrice * 0.008);
      data.push({ time: d === 0 ? weeks[w] : '', price: Number(base.toFixed(2)) });
    }
  }
  for (let d = 0; d < 5; d++) {
    base = base + ((currentPrice - base) / (5 - d)) + (Math.random() - 0.5) * 0.8;
    data.push({ time: d === 2 ? 'EVENT' : d === 4 ? 'Wk 4' : '', price: Number(base.toFixed(2)) });
  }
  const startPrice = data[0].price;
  const endPrice = data[data.length - 1].price;
  const delta = Number((endPrice - startPrice).toFixed(2));
  const changePct = Number(((delta / startPrice) * 100).toFixed(2));
  return { data, eventMarker: 'EVENT', changePct, delta, currentPrice: endPrice, periodLabel: 'Past Month' };
}
