const sortArray = (nums: number[]): number[] => {
    return mergeSort(nums)
};

const mergeSort = (nums:number[]) : number[]=> {
    if (nums.length <= 1) return nums;

    let midle_ind = Math.floor(nums.length / 2);
    let left_part = nums.slice(0, midle_ind);
    let right_part = nums.slice(midle_ind);
    
    let sortedLeft = mergeSort(left_part);
    let sortedRight = mergeSort(right_part);
    
    return merge(sortedLeft, sortedRight);
}

const merge = (array1: number[], array2: number[]): number[]=> {
    let p1=0, p2=0;
    let result = [];

    while(p1 < array1.length && p2 < array2.length) {
        if (array1[p1] < array2[p2]) result.push[array1[p1++]];
        else result.push[array2[p2++]];
    }

    return result.concat(array1.slice(p1), array2.slice(p2))
}

