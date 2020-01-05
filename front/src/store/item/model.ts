import { observable } from 'mobx';

export default class ItemModel {
  id: number;
  @observable title: string;
  @observable content: string;

  constructor(
    id: number,
    title: string,
    content: string,
  ) {
    this.id = id;
    this.title = title;
    this.content = content;
  }
}
